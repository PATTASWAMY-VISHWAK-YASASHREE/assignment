import pytest
from unittest.mock import MagicMock, patch
from app.services import dataset_service

@pytest.mark.asyncio
async def test_save_dataset_optimizes_memory_usage():
    # Mock UploadFile
    mock_file = MagicMock()
    mock_file.filename = "test.csv"

    # Mock the underlying file object (SpooledTemporaryFile)
    mock_spooled_file = MagicMock()
    mock_file.file = mock_spooled_file

    # Setup seek/tell for size check
    # mock_spooled_file.seek does nothing
    mock_spooled_file.tell.return_value = 100 # 100 bytes

    # mocking read to ensure it's NOT called on the UploadFile wrapper (which does chunked read)
    # The original implementation calls `await file.read(chunk_size)`
    # We want to ensure that is NOT called.
    mock_file.read = MagicMock()

    # We also need to mock _read_dataframe to avoid actual pandas processing of our mock file
    # and to verify it receives the file object
    with patch("app.services.dataset_service._read_dataframe") as mock_read_df:
        mock_read_df.return_value = MagicMock(empty=False, shape=(10, 2), columns=["a", "b"], dtypes={"a": "int", "b": "int"})
        # The mock dataframe needs to support head().fillna().to_dict() chain
        mock_read_df.return_value.head.return_value.fillna.return_value.to_dict.return_value = []

        await dataset_service.save_dataset(mock_file)

        # Verification

        # 1. verify `file.read` was NOT called (meaning we didn't chunk-read into memory)
        mock_file.read.assert_not_called()

        # 2. verify `file.file.seek` WAS called (for size check)
        # It should be called with (0, 2) to go to end, and (0) to rewind.
        mock_spooled_file.seek.assert_any_call(0, 2)
        mock_spooled_file.seek.assert_any_call(0)

        # 3. verify _read_dataframe was called with the underlying file object
        mock_read_df.assert_called_once()
        args, _ = mock_read_df.call_args
        # args[0] is filename, args[1] is the file object (previously content bytes)
        assert args[1] == mock_spooled_file
