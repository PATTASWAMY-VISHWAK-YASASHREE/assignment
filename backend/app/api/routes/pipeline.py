from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.pipeline import (
    PipelineRunRequest,
    PipelineRunResponse,
    PredictRequest,
    PredictResponse,
)
from app.services import pipeline_service

router = APIRouter(tags=["pipeline"])


@router.post("/pipeline/run", response_model=PipelineRunResponse)
async def run_pipeline(payload: PipelineRunRequest):
    try:
        return await pipeline_service.run_pipeline(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - defensive catch for unexpected issues
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {exc}")


@router.post("/pipeline/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    try:
        return await pipeline_service.predict(payload.model_id, payload.records)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")


@router.get("/pipeline/model/{model_id}/download")
async def download_model(model_id: str):
    try:
        content = pipeline_service.download_model_bytes(model_id)
        return StreamingResponse(
            BytesIO(content),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=model-{model_id}.pkl"},
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Download failed: {exc}")
