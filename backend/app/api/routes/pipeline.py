from fastapi import APIRouter, HTTPException

from app.schemas.pipeline import PipelineRunRequest, PipelineRunResponse
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
