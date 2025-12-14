from __future__ import annotations

from io import BytesIO
from typing import Dict
from uuid import uuid4

import pandas as pd
from fastapi import UploadFile

from app.schemas.dataset import DatasetUploadResponse

_dataset_store: Dict[str, pd.DataFrame] = {}


def _read_dataframe(file: UploadFile, content: bytes) -> pd.DataFrame:
    filename = file.filename or ""
    lowered = filename.lower()
    if lowered.endswith(".csv"):
        return pd.read_csv(BytesIO(content))
    if lowered.endswith(".xlsx") or lowered.endswith(".xls"):
        return pd.read_excel(BytesIO(content))
    raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")


def get_dataset(dataset_id: str) -> pd.DataFrame:
    if dataset_id not in _dataset_store:
        raise ValueError("Dataset not found. Please upload again.")
    return _dataset_store[dataset_id]


async def save_dataset(file: UploadFile) -> DatasetUploadResponse:
    content = await file.read()
    if not content:
        raise ValueError("Uploaded file is empty.")

    df = _read_dataframe(file, content)
    if df.empty:
        raise ValueError("Dataset contains no rows.")

    dataset_id = str(uuid4())
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
