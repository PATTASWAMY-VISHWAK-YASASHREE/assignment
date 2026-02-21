import asyncio
from unittest.mock import MagicMock, patch
import pytest
from starlette.datastructures import UploadFile
from app.services import dataset_service

@pytest.mark.asyncio
async def test_save_dataset_optimizes_memory():
    # Mock the file object (BytesIO-like)
    mock_file_obj = MagicMock()
    # Simulate valid file behavior
    mock_file_obj.read.return_value = b""
    mock_file_obj.tell.return_value = 100

    # Create UploadFile with mocked file
    upload = UploadFile(filename="test.csv", file=mock_file_obj)

    # We mock the _read_dataframe function to verify it receives the file object
    with patch("app.services.dataset_service._read_dataframe") as mock_read_df:
        # return a mock dataframe
        mock_df = MagicMock()
        mock_df.empty = False
        mock_df.shape = (10, 2)
        mock_df.columns = ["a", "b"]
        mock_df.dtypes = {"a": "int", "b": "int"}
        mock_df.head.return_value.fillna.return_value.to_dict.return_value = []
        mock_read_df.return_value = mock_df

        # Run the function
        await dataset_service.save_dataset(upload)

        # Verification:
        # 1. Ensure we sought to end and back to start
        mock_file_obj.seek.assert_any_call(0, 2) # Seek end
        mock_file_obj.seek.assert_any_call(0)    # Seek start

        # 2. Ensure we checked size
        assert mock_file_obj.tell.called

        # 3. Ensure _read_dataframe was called with the file object, not bytes
        args, _ = mock_read_df.call_args
        # args[0] is filename, args[1] is content
        assert args[0] == "test.csv"
        # The key check: verify we passed the file object, not a bytes object
        assert args[1] is mock_file_obj
