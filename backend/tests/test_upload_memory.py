import asyncio
from unittest.mock import MagicMock, patch
import pytest
from starlette.datastructures import UploadFile
from app.services import dataset_service

@pytest.mark.asyncio
async def test_save_dataset_does_not_read_content_into_memory():
    """
    Verifies that save_dataset checks size using seek/tell and does not
    manually read the file content into a bytearray before processing.
    """
    # Mock file object with seek/tell support
    mock_file = MagicMock()
    # Mock tell to return a valid size (e.g. 100 bytes)
    mock_file.tell.return_value = 100

    # UploadFile wrapper
    # We must mock 'filename' attribute explicitly if passing mock_file directly doesn't suffice
    # but UploadFile constructor handles it.
    upload = UploadFile(filename="test.csv", file=mock_file)

    # Mock pandas read_csv so we don't need to provide valid CSV data
    # and we can verify what was passed to it.
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.shape = (5, 2)
    mock_df.columns = ["a", "b"]
    # dtypes needs to support .items()
    mock_df.dtypes = {"a": "int", "b": "int"}

    # chained calls
    mock_df.head.return_value = mock_df
    mock_df.fillna.return_value = mock_df
    mock_df.to_dict.return_value = [{"a": 1, "b": 2}]

    with patch("app.services.dataset_service.pd.read_csv") as mock_read_csv:
        mock_read_csv.return_value = mock_df

        await dataset_service.save_dataset(upload)

        # Verify seek/tell were used for size check
        mock_file.seek.assert_any_call(0, 2)
        mock_file.tell.assert_called()
        mock_file.seek.assert_any_call(0)

        # Verify that we did NOT call read() on the file object in the service logic
        # (The service passes the file to pandas, but since pandas is mocked,
        #  nothing should have read from the file).
        mock_file.read.assert_not_called()

        # Verify that pandas.read_csv was called with the file object directly
        # Note: run_in_executor might make direct assert_called_with tricky if arguments are copied/pickled?
        # But here we pass the object by reference (threads share memory).
        mock_read_csv.assert_called()
        args, _ = mock_read_csv.call_args
        # The first argument passed to read_csv should be our mock_file
        assert args[0] is mock_file

@pytest.mark.asyncio
async def test_save_dataset_large_file_rejection_no_read():
    """
    Verifies that a large file is rejected via seek/tell without reading it.
    """
    mock_file = MagicMock()
    # Mock tell to return a size larger than default MAX (100MB)
    # 101 MB
    mock_file.tell.return_value = 101 * 1024 * 1024

    upload = UploadFile(filename="large.csv", file=mock_file)

    with pytest.raises(ValueError, match="Uploaded file exceeds"):
        await dataset_service.save_dataset(upload)

    # Verify seek/tell usage
    mock_file.seek.assert_any_call(0, 2)
    mock_file.tell.assert_called()

    # Verify read was never called
    mock_file.read.assert_not_called()
