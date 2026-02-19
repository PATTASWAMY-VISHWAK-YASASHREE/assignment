import pytest
from unittest.mock import MagicMock, AsyncMock
from starlette.datastructures import UploadFile
from io import BytesIO
from app.services import dataset_service


@pytest.mark.asyncio
async def test_save_dataset_no_memory_copy():
    # Mock file content
    content = b"col1,col2\n1,2"
    file_mock = BytesIO(content)

    # Create UploadFile
    upload = UploadFile(filename="test.csv", file=file_mock)

    # Spy on read method
    # Note: UploadFile.read is an async method
    upload.read = AsyncMock(wraps=upload.read)

    # Spy on seek method of the underlying file
    # file_mock.seek is a synchronous method
    file_mock.seek = MagicMock(wraps=file_mock.seek)

    # Call the function
    await dataset_service.save_dataset(upload)

    # Assertions
    # In the optimized version, we expect 0 calls to read()
    assert upload.read.call_count == 0, "Should not call read() on UploadFile"

    # We expect calls to seek() on the underlying file (0, 2) and (0, 0)
    # The exact number depends on implementation, but at least 2.
    # checking size: seek(0, 2) -> seek(0)
    # pandas read_csv might seek too.
    assert file_mock.seek.call_count >= 2, (
        "Should call seek() on underlying file for size check"
    )
