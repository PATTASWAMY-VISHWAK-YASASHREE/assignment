import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from io import BytesIO

from app.api.routes.datasets import router
from app.schemas.dataset import DatasetUploadResponse


# Setup test app
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    content = b"col1,col2,col3\n1,2,3\n4,5,6"
    return {"file": ("test_dataset.csv", BytesIO(content), "text/csv")}


@pytest.fixture
def sample_dataset_response():
    """Sample successful response data."""
    return DatasetUploadResponse(
        dataset_id="dataset-123",
        rows=2,
        columns=3,
        column_names=["col1", "col2", "col3"],
        dtypes={"col1": "int64", "col2": "int64", "col3": "int64"},
        preview=[{"col1": 1, "col2": 2, "col3": 3}],
    )


class TestUploadDataset:
    """Tests for POST /datasets/upload endpoint."""

    # ==================== Success Cases ====================

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_success(
        self, mock_save_dataset, client, sample_csv_file, sample_dataset_response
    ):
        """Test successful dataset upload returns 200 with dataset info."""
        mock_save_dataset.return_value = sample_dataset_response

        response = client.post("/datasets/upload", files=sample_csv_file)

        assert response.status_code == 200
        data = response.json()
        assert data["dataset_id"] == "dataset-123"
        assert data["rows"] == 2
        assert data["columns"] == 3
        mock_save_dataset.assert_called_once()

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_service_called_with_file(
        self, mock_save_dataset, client, sample_csv_file, sample_dataset_response
    ):
        """Test that dataset service is called with the uploaded file."""
        mock_save_dataset.return_value = sample_dataset_response

        client.post("/datasets/upload", files=sample_csv_file)

        # Verify service was called
        mock_save_dataset.assert_called_once()
        call_args = mock_save_dataset.call_args
        uploaded_file = call_args[0][0]
        assert uploaded_file.filename == "test_dataset.csv"

    # ==================== Validation Error Cases (400) ====================

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_invalid_format_returns_400(
        self, mock_save_dataset, client, sample_csv_file
    ):
        """Test that ValueError from service returns 400 status."""
        mock_save_dataset.side_effect = ValueError("Invalid file format")

        response = client.post("/datasets/upload", files=sample_csv_file)

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid file format"

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_empty_file_returns_400(
        self, mock_save_dataset, client
    ):
        """Test that empty file validation error returns 400."""
        mock_save_dataset.side_effect = ValueError("File is empty")
        empty_file = {"file": ("empty.csv", BytesIO(b""), "text/csv")}

        response = client.post("/datasets/upload", files=empty_file)

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_unsupported_type_returns_400(
        self, mock_save_dataset, client
    ):
        """Test that unsupported file type returns 400."""
        mock_save_dataset.side_effect = ValueError(
            "Unsupported file type. Only CSV and Excel files are allowed"
        )
        exe_file = {"file": ("malware.exe", BytesIO(b"binary"), "application/x-msdownload")}

        response = client.post("/datasets/upload", files=exe_file)

        assert response.status_code == 400
        assert "Unsupported" in response.json()["detail"]

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_corrupted_file_returns_400(
        self, mock_save_dataset, client
    ):
        """Test that corrupted file returns 400."""
        mock_save_dataset.side_effect = ValueError("Failed to parse file: corrupted data")
        corrupted_file = {"file": ("bad.csv", BytesIO(b"\x00\x01\x02"), "text/csv")}

        response = client.post("/datasets/upload", files=corrupted_file)

        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to parse file: corrupted data"

    # ==================== Server Error Cases (500) ====================

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_unexpected_error_returns_500(
        self, mock_save_dataset, client, sample_csv_file
    ):
        """Test that unexpected exceptions return 500 status."""
        mock_save_dataset.side_effect = RuntimeError("Database connection failed")

        response = client.post("/datasets/upload", files=sample_csv_file)

        assert response.status_code == 500
        assert "Failed to process dataset" in response.json()["detail"]
        assert "Database connection failed" in response.json()["detail"]

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_dataset_io_error_returns_500(
        self, mock_save_dataset, client, sample_csv_file
    ):
        """Test that IO errors return 500 status."""
        mock_save_dataset.side_effect = IOError("Disk full")

        response = client.post("/datasets/upload", files=sample_csv_file)

        assert response.status_code == 500
        assert "Failed to process dataset" in response.json()["detail"]

    # ==================== Missing File Cases (422) ====================

    def test_upload_dataset_no_file_returns_422(self, client):
        """Test that missing file returns 422 validation error."""
        response = client.post("/datasets/upload")

        assert response.status_code == 422

    def test_upload_dataset_wrong_field_name_returns_422(self, client):
        """Test that wrong field name returns 422 validation error."""
        wrong_field = {"wrong_name": ("test.csv", BytesIO(b"data"), "text/csv")}

        response = client.post("/datasets/upload", files=wrong_field)

        assert response.status_code == 422

    # ==================== Different File Types ====================

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_excel_file_success(
        self, mock_save_dataset, client, sample_dataset_response
    ):
        """Test successful Excel file upload."""
        mock_save_dataset.return_value = sample_dataset_response
        excel_file = {"file": ("data.xlsx", BytesIO(b"excel-content"), 
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

        response = client.post("/datasets/upload", files=excel_file)

        assert response.status_code == 200
        mock_save_dataset.assert_called_once()

    @patch("app.api.routes.datasets.dataset_service.save_dataset")
    def test_upload_large_filename(
        self, mock_save_dataset, client, sample_dataset_response
    ):
        """Test upload with very long filename."""
        mock_save_dataset.return_value = sample_dataset_response
        long_name = "a" * 200 + ".csv"
        file_with_long_name = {"file": (long_name, BytesIO(b"data"), "text/csv")}

        response = client.post("/datasets/upload", files=file_with_long_name)

        assert response.status_code == 200


# ==================== Async Tests (for pytest-asyncio) ====================

@pytest.mark.asyncio
class TestUploadDatasetAsync:
    """Async tests for the upload endpoint."""

    @patch("app.api.routes.datasets.dataset_service.save_dataset", new_callable=AsyncMock)
    async def test_async_service_call(
        self, mock_save_dataset, app, sample_dataset_response
    ):
        """Test that async service is properly awaited."""
        from httpx import AsyncClient, ASGITransport
        
        mock_save_dataset.return_value = sample_dataset_response
        
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/datasets/upload",
                files={"file": ("test.csv", b"col1\n1", "text/csv")}
            )
        
        assert response.status_code == 200
        mock_save_dataset.assert_awaited_once()