import asyncio
from io import BytesIO
from unittest.mock import patch
import pytest
from starlette.datastructures import UploadFile
from app.services import dataset_service
from app.core.config import settings

@pytest.mark.asyncio
async def test_save_dataset_rejects_large_file():
    # Create a 2KB file
    content = b"a" * 2048
    upload = UploadFile(filename="large.csv", file=BytesIO(content))

    # Mock MAX_UPLOAD_SIZE_BYTES to 1KB (1024 bytes)
    with patch("app.core.config.settings.MAX_UPLOAD_SIZE_BYTES", 1024):
        # Verify it raises ValueError
        try:
            await dataset_service.save_dataset(upload)
            pytest.fail("Should have raised ValueError for large file")
        except ValueError as e:
            assert str(e) == "Uploaded file exceeds the maximum allowed size of 1024 bytes."
        except Exception as e:
            pytest.fail(f"Raised unexpected exception: {e}")

@pytest.mark.asyncio
async def test_save_dataset_accepts_valid_size_file():
    # Create a 512B file (valid)
    content = b"a" * 512
    # It needs to be a valid CSV to pass _read_dataframe check
    content = b"col1,col2\n1,2\n" * 50 # roughly 500 bytes
    upload = UploadFile(filename="valid.csv", file=BytesIO(content))

    # Mock MAX_UPLOAD_SIZE_BYTES to 1KB (1024 bytes)
    with patch("app.core.config.settings.MAX_UPLOAD_SIZE_BYTES", 1024):
        response = await dataset_service.save_dataset(upload)
        assert response.dataset_id is not None
