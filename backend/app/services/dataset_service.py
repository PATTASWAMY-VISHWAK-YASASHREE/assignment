from __future__ import annotations

import asyncio
from typing import Dict, BinaryIO
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


def _read_dataframe(filename: str, file_obj: BinaryIO) -> pd.DataFrame:
    lowered = filename.lower()
    if lowered.endswith(".csv"):
        return pd.read_csv(file_obj)
    if lowered.endswith(".xlsx") or lowered.endswith(".xls"):
        return pd.read_excel(file_obj)
    raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")


def get_dataset(dataset_id: str) -> pd.DataFrame:
    with _dataset_lock:
        if dataset_id not in _dataset_store:
            raise ValueError("Dataset not found. Please upload again.")
        return _dataset_store[dataset_id]


async def save_dataset(file: UploadFile) -> DatasetUploadResponse:
    # Check file size by seeking to the end to avoid reading into memory
    MAX_SIZE = settings.MAX_UPLOAD_SIZE_BYTES

    # Ensure file is at start
    file.file.seek(0)

    # Seek to end to get size
    file.file.seek(0, 2)
    size = file.file.tell()

    # Reset to start for reading
    file.file.seek(0)

    if size > MAX_SIZE:
        raise ValueError(
            f"Uploaded file exceeds the maximum allowed size of {MAX_SIZE} bytes."
        )

    if size == 0:
        raise ValueError("Uploaded file is empty.")

    filename = file.filename or ""
    loop = asyncio.get_running_loop()

    # Offload blocking IO/CPU task to a thread pool
    # Pass the underlying file object directly to pandas to avoid memory copy
    # file.file is the synchronous SpooledTemporaryFile object
    df = await loop.run_in_executor(None, _read_dataframe, filename, file.file)

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
