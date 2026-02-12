from __future__ import annotations

import asyncio
from io import BytesIO
from typing import Dict
from threading import RLock
from uuid import uuid4

import pandas as pd
from fastapi import UploadFile

from app.schemas.dataset import DatasetUploadResponse

# WARNING: _dataset_store is protected by _dataset_lock.
# Direct access to _dataset_store is NOT thread-safe and should only be done in tests.
# All production code must access datasets via get_dataset and save_dataset.
_dataset_store: Dict[str, pd.DataFrame] = {}
_dataset_lock = RLock()


def _read_dataframe(filename: str, content: bytes) -> pd.DataFrame:
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
    content = await file.read()
    if not content:
        raise ValueError("Uploaded file is empty.")

    filename = file.filename or ""
    loop = asyncio.get_running_loop()
    # Offload blocking IO/CPU task to a thread pool
    df = await loop.run_in_executor(None, _read_dataframe, filename, content)

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
