from __future__ import annotations

from io import BytesIO
from typing import Dict
from threading import RLock
from uuid import uuid4

import pandas as pd
from fastapi import UploadFile

from app.schemas.dataset import DatasetUploadResponse
from app.core.config import settings

# WARNING: _dataset_store is protected by _dataset_lock.
# Direct access to _dataset_store is NOT thread-safe and should only be done in tests.
# All production code must access datasets via get_dataset and save_dataset.
_dataset_store: Dict[str, pd.DataFrame] = {}
_dataset_lock = RLock()


def _read_dataframe(file: UploadFile, content: bytes) -> pd.DataFrame:
    filename = file.filename or ""
    lowered = filename.lower()
    if lowered.endswith(".csv"):
        return pd.read_csv(BytesIO(content))
    if lowered.endswith(".xlsx") or lowered.endswith(".xls"):
        return pd.read_excel(BytesIO(content))
    raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")


def get_dataset(dataset_id: str) -> pd.DataFrame:
    with _dataset_lock:
        if dataset_id not in _dataset_store:
            raise ValueError("Dataset not found. Please upload again.")
        return _dataset_store[dataset_id]


async def save_dataset(file: UploadFile) -> DatasetUploadResponse:
    # Check file size by reading in chunks to avoid memory exhaustion
    # and to validate size before processing.
    MAX_SIZE = settings.MAX_UPLOAD_SIZE_BYTES
    chunk_size = 1024 * 1024  # 1MB chunks
    content = bytearray()

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        content.extend(chunk)
        if len(content) > MAX_SIZE:
            raise ValueError(
                f"Uploaded file exceeds the maximum allowed size of {MAX_SIZE} bytes."
            )

    if not content:
        raise ValueError("Uploaded file is empty.")

    # Convert bytearray back to bytes for compatibility
    content = bytes(content)

    df = _read_dataframe(file, content)
    if df.empty:
        raise ValueError("Dataset contains no rows.")

    dataset_id = str(uuid4())
    with _dataset_lock:
        _dataset_store[dataset_id] = df

    preview = df.head(5).fillna("null").to_dict(orient="records")
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    return DatasetUploadResponse(
        dataset_id=dataset_id,
        rows=df.shape[0],
        columns=df.shape[1],
        column_names=list(df.columns),
        dtypes=dtypes,
        preview=preview,
    )
