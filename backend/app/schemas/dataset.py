from typing import List, Dict

from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    dataset_id: str
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]


class DatasetUploadResponse(DatasetMetadata):
    preview: List[Dict[str, object]]
