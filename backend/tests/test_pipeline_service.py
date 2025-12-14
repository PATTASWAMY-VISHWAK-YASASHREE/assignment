import asyncio

import pandas as pd
import pytest

from app.schemas.pipeline import (
    ConfusionMatrix,
    ModelType,
    PipelineRunRequest,
    PreprocessStep,
    PreprocessType,
    TrainTestConfig,
)
from app.services import dataset_service, pipeline_service


def _store_dataset(df: pd.DataFrame) -> str:
    dataset_id = "test-dataset"
    dataset_service._dataset_store[dataset_id] = df
    return dataset_id


def test_run_pipeline_success(sample_dataframe):
    dataset_id = _store_dataset(sample_dataframe)

    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["feature1", "feature2"],
        preprocess=[PreprocessStep(step=PreprocessType.standardize)],
        split=TrainTestConfig(test_size=0.34, random_state=0),
        model=ModelType.logistic_regression,
    )

    response = asyncio.run(pipeline_service.run_pipeline(request))

    assert response.status == "success"
    assert response.model_type == ModelType.logistic_regression
    assert 0.0 <= response.accuracy <= 1.0
    assert isinstance(response.confusion_matrix, ConfusionMatrix)
    assert len(response.confusion_matrix.labels) == 2
    assert response.feature_importances is not None
    assert len(response.feature_importances) > 0
    assert response.warnings == []


def test_run_pipeline_missing_target_column(sample_dataframe):
    dataset_id = _store_dataset(sample_dataframe)
    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="missing",
        feature_columns=["feature1"],
        preprocess=[],
        split=TrainTestConfig(),
        model=ModelType.decision_tree,
    )

    with pytest.raises(ValueError, match="Target column not found"):
        asyncio.run(pipeline_service.run_pipeline(request))


def test_run_pipeline_no_feature_columns():
    df = pd.DataFrame({"target": [0, 1, 0, 1]})
    dataset_id = _store_dataset(df)
    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=None,
        preprocess=[],
        split=TrainTestConfig(),
        model=ModelType.decision_tree,
    )

    with pytest.raises(ValueError, match="No feature columns selected"):
        asyncio.run(pipeline_service.run_pipeline(request))


def test_run_pipeline_warns_on_non_numeric_preprocess():
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4],
            "category": ["a", "b", "a", "b"],
            "target": [0, 1, 0, 1],
        }
    )
    dataset_id = _store_dataset(df)
    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["feature1", "category"],
        preprocess=[PreprocessStep(step=PreprocessType.standardize, columns=["feature1", "category"])],
        split=TrainTestConfig(test_size=0.5, random_state=1),
        model=ModelType.logistic_regression,
    )

    response = asyncio.run(pipeline_service.run_pipeline(request))

    assert any("Skipped non-numeric" in msg for msg in response.warnings)
    assert response.accuracy is not None


def test_run_pipeline_drops_rare_classes_when_enabled(sample_dataframe):
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0, 0, 0, 1]})
    dataset_id = _store_dataset(df)
    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["f1"],
        preprocess=[],
        split=TrainTestConfig(test_size=0.25, random_state=0),
        model=ModelType.logistic_regression,
        drop_rare_classes=True,
    )

    response = asyncio.run(pipeline_service.run_pipeline(request))

    assert response.status == "success"
    assert any("Dropped classes" in w for w in response.warnings)


def test_run_pipeline_rare_classes_error_without_drop(sample_dataframe):
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0, 0, 0, 1]})
    dataset_id = _store_dataset(df)
    request = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["f1"],
        preprocess=[],
        split=TrainTestConfig(test_size=0.25, random_state=0),
        model=ModelType.logistic_regression,
        drop_rare_classes=False,
    )

    with pytest.raises(ValueError, match="least populated classes"):
        asyncio.run(pipeline_service.run_pipeline(request))
