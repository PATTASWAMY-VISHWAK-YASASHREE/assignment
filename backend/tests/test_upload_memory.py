import asyncio
from unittest.mock import MagicMock, patch
import pytest
from starlette.datastructures import UploadFile
from app.services import dataset_service

@pytest.mark.asyncio
async def test_save_dataset_optimizes_memory_usage():
    """
    Verifies that save_dataset uses seek/tell for size checks instead of reading
    the file into memory, and passes the file object directly to pandas.
    """
    # Mock the internal file object (SpooledTemporaryFile)
    mock_file = MagicMock()
    # Simulate file size of 100 bytes
    mock_file.tell.return_value = 100

    # Mock UploadFile
    upload = UploadFile(filename="test.csv", file=mock_file)

    # Mock _read_dataframe to avoid actual pandas processing
    # We return a dummy dataframe structure
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.shape = (10, 2)
    mock_df.columns = ["col1", "col2"]
    mock_df.dtypes = {"col1": "int", "col2": "int"}
    mock_df.head.return_value.fillna.return_value.to_dict.return_value = []

    with patch("app.services.dataset_service._read_dataframe", return_value=mock_df) as mock_read_df:
        await dataset_service.save_dataset(upload)

        # Verify seek/tell were used for size check
        # First seek(0, 2) to end
        mock_file.seek.assert_any_call(0, 2)
        # Then tell() to get size
        assert mock_file.tell.called
        # Then seek(0) to rewind
        mock_file.seek.assert_any_call(0)

        # Verify read was NOT called on the file object directly by save_dataset loop
        # (The old implementation called read() in a loop)
        mock_file.read.assert_not_called()

        # Verify the file object was passed directly to _read_dataframe
        mock_read_df.assert_called_once()
        call_args = mock_read_df.call_args
        # args[0] is filename, args[1] is file_obj
        assert call_args[0][1] == mock_file
