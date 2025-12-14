from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator


class PreprocessType(str, Enum):
    standardize = "standardize"
    normalize = "normalize"


class ModelType(str, Enum):
    logistic_regression = "logistic_regression"
    decision_tree = "decision_tree"


class PreprocessStep(BaseModel):
    step: PreprocessType
    columns: Optional[List[str]] = None


class TrainTestConfig(BaseModel):
    test_size: float = Field(0.2, ge=0.05, le=0.95)
    random_state: int = 42


class PipelineRunRequest(BaseModel):
    dataset_id: str
    target_column: str
    feature_columns: Optional[List[str]] = None
    preprocess: List[PreprocessStep] = Field(default_factory=list)
    split: TrainTestConfig = Field(default_factory=TrainTestConfig)
    model: ModelType
    drop_rare_classes: bool = False

    @field_validator("feature_columns", mode="before")
    def ensure_features(cls, value):
        """
        Normalize empty/absent feature selections to ``None``.

        ``mode="before"`` runs prior to Pydantic's own parsing so we can turn
        an empty list (or missing value) into ``None`` before any further
        validation. This keeps downstream logic simple because we only need to
        check for ``None`` instead of handling both ``None`` and ``[]``.
        """
        if value is None or (isinstance(value, list) and len(value) == 0):
            return None
        return value


class ConfusionMatrix(BaseModel):
    labels: List[Any]
    matrix: List[List[int]]


class FeatureImportance(BaseModel):
    name: str
    importance: float


class PipelineRunResponse(BaseModel):
    status: str
    accuracy: Optional[float] = None
    confusion_matrix: Optional[ConfusionMatrix] = None
    feature_importances: Optional[List[FeatureImportance]] = None
    message: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    model_type: Optional[ModelType] = None
    model_id: Optional[str] = None
    model_download_path: Optional[str] = None


class PredictRequest(BaseModel):
    model_id: str
    records: List[Dict[str, Any]]


class PredictResponse(BaseModel):
    predictions: List[Any]
