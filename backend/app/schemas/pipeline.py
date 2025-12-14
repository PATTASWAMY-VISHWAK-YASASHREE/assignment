from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, validator


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

    @validator("feature_columns", always=True)
    def ensure_features(cls, v, values):
        if v is None:
            return None
        if len(v) == 0:
            return None
        return v


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
