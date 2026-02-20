import asyncio
from unittest.mock import MagicMock, AsyncMock
import pytest
import pandas as pd
from starlette.datastructures import UploadFile
from app.services import dataset_service

@pytest.mark.asyncio
async def test_save_dataset_uses_seek_and_stream():
    # Mock the underlying file object
    mock_file = MagicMock()
    # Mock behavior for seek/tell to simulate size check
    mock_file.seek = MagicMock()
    mock_file.tell = MagicMock(return_value=100) # 100 bytes

    # Mock UploadFile
    upload = UploadFile(filename="test.csv", file=mock_file)
    # AsyncMock read method correctly
    upload.read = AsyncMock(return_value=b"")

    # We also need to mock `dataset_service._read_dataframe` because it will try to read from our mock_file
    # and we don't want to actually run pandas on a mock.

    original_read_dataframe = dataset_service._read_dataframe
    dataset_service._read_dataframe = MagicMock(return_value=pd.DataFrame({'a': [1], 'b': [2]}))

    try:
        # Run the function
        await dataset_service.save_dataset(upload)

        # Verify optimization:
        # 1. upload.read should NOT be called (we access file.file directly)
        upload.read.assert_not_called()

        # 2. file.file.seek should be called (for size check)
        assert mock_file.seek.called

        # 3. _read_dataframe should be called with the mock_file (stream), not bytes
        dataset_service._read_dataframe.assert_called_once()
        args = dataset_service._read_dataframe.call_args[0]
        # args[0] is filename, args[1] should be the file object
        assert args[1] == mock_file

    except Exception as e:
        # If it fails because upload.read WAS called, then we haven't optimized it yet (which is expected)
        # We can just fail the test to confirm we need to implement the optimization.
        # But if it fails for other reasons, we need to know.
        if "assert_not_called" in str(e):
            pytest.fail("Optimization NOT implemented: upload.read() was called")
        elif "assert_called_once" in str(e):
             pytest.fail("Optimization NOT implemented: _read_dataframe not called with stream")
        else:
             pytest.fail(f"Optimization test failed with unexpected error: {e}")
    finally:
        dataset_service._read_dataframe = original_read_dataframe
