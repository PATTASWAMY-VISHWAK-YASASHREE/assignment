from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.dataset import DatasetUploadResponse
from app.services import dataset_service

router = APIRouter(tags=["datasets"])


@router.post("/datasets/upload", response_model=DatasetUploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    try:
        dataset_info = await dataset_service.save_dataset(file)
        return dataset_info
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - defensive catch for unexpected issues
        raise HTTPException(status_code=500, detail=f"Failed to process dataset: {exc}")
