import asyncio
from io import BytesIO

import pandas as pd
import pytest
from starlette.datastructures import UploadFile

from app.schemas.dataset import DatasetUploadResponse
from app.services import dataset_service


def _upload_file(name: str, content: bytes) -> UploadFile:
    return UploadFile(filename=name, file=BytesIO(content))


def test_save_dataset_rejects_empty_file():
    upload = _upload_file("empty.csv", b"")
    with pytest.raises(ValueError, match="Uploaded file is empty"):
        asyncio.run(dataset_service.save_dataset(upload))


def test_save_dataset_rejects_unsupported_format():
    upload = _upload_file("notes.txt", b"hello world")
    with pytest.raises(ValueError, match="Unsupported file format"):
        asyncio.run(dataset_service.save_dataset(upload))


def test_save_dataset_csv_success(sample_csv_bytes):
    upload = _upload_file("data.csv", sample_csv_bytes)
    response = asyncio.run(dataset_service.save_dataset(upload))

    assert isinstance(response, DatasetUploadResponse)
    assert response.rows == 6
    assert response.columns == 3
    assert set(response.column_names) == {"feature1", "feature2", "target"}
    assert len(response.preview) <= 5

    stored = dataset_service.get_dataset(response.dataset_id)
    assert isinstance(stored, pd.DataFrame)
    assert stored.equals(pd.read_csv(BytesIO(sample_csv_bytes)))


def test_get_dataset_raises_for_missing_id():
    with pytest.raises(ValueError, match="Dataset not found"):
        dataset_service.get_dataset("missing-id")


def test_save_dataset_xlsx_success(sample_dataframe):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        sample_dataframe.to_excel(writer, index=False)
    buffer.seek(0)

    upload = _upload_file("data.xlsx", buffer.read())
    response = asyncio.run(dataset_service.save_dataset(upload))

    assert response.columns == sample_dataframe.shape[1]
    assert response.rows == sample_dataframe.shape[0]
    stored = dataset_service.get_dataset(response.dataset_id)
    assert stored.equals(sample_dataframe)


@pytest.mark.asyncio
async def test_concurrent_saves_generate_unique_ids(sample_csv_bytes):
    async def _save_once():
        upload = _upload_file("data.csv", sample_csv_bytes)
        return await dataset_service.save_dataset(upload)

    results = await asyncio.gather(*[_save_once() for _ in range(5)])
    ids = {res.dataset_id for res in results}

    assert len(ids) == 5
    # ensure store has all entries
    for res in results:
        retrieved = dataset_service.get_dataset(res.dataset_id)
        assert isinstance(retrieved, pd.DataFrame)
