import asyncio
from io import BytesIO

import numpy as np
import pandas as pd
import pytest
from starlette.datastructures import UploadFile

from app.schemas.pipeline import (
    ModelType,
    PipelineRunRequest,
    PreprocessStep,
    PreprocessType,
    TrainTestConfig,
)
from app.services import dataset_service, pipeline_service


def _upload_file(name: str, content: bytes) -> UploadFile:
    return UploadFile(filename=name, file=BytesIO(content))


# 1) Dataset service: rejects dataset with headers only (no rows)
def test_save_dataset_rejects_header_only_csv():
    csv_bytes = b"feature1,feature2,target\n"
    upload = _upload_file("data.csv", csv_bytes)
    with pytest.raises(ValueError, match="contains no rows"):
        asyncio.run(dataset_service.save_dataset(upload))


# 2) Pipeline: default features when feature_columns is omitted

def test_pipeline_uses_all_non_target_features_when_none_provided():
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "target": [0, 1, 0, 1, 0, 1],
        }
    )
    dataset_id = "dataset-auto-features"
    dataset_service._dataset_store[dataset_id] = df

    req = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=None,  # should default to all non-target columns
        preprocess=[],
        split=TrainTestConfig(test_size=0.34, random_state=0),
        model=ModelType.decision_tree,
    )

    resp = asyncio.run(pipeline_service.run_pipeline(req))
    assert resp.status == "success"
    assert resp.model_type == ModelType.decision_tree
    assert 0.0 <= resp.accuracy <= 1.0


# 3) Pipeline: imputes missing target with mode and logs warning

def test_pipeline_imputes_missing_target_and_warns():
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "target": [0, 1, np.nan, 1, 0, np.nan],
        }
    )
    dataset_id = "dataset-missing-target"
    dataset_service._dataset_store[dataset_id] = df

    req = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["feature1", "feature2"],
        preprocess=[],
        split=TrainTestConfig(test_size=0.34, random_state=0),
        model=ModelType.logistic_regression,
    )

    resp = asyncio.run(pipeline_service.run_pipeline(req))
    assert any("Missing target values filled with mode" in w for w in resp.warnings)
    assert resp.accuracy is not None


# 4) Pipeline: standardization applied only to numeric and warns for non-numeric selected explicitly

def test_pipeline_warns_and_skips_non_numeric_in_preprocess():
    df = pd.DataFrame(
        {
            "num": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "cat": ["a", "b", "a", "b", "a", "b"],
            "target": [0, 1, 0, 1, 0, 1],
        }
    )
    dataset_id = "dataset-preprocess-warn"
    dataset_service._dataset_store[dataset_id] = df

    req = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["num", "cat"],
        preprocess=[PreprocessStep(step=PreprocessType.standardize, columns=["num", "cat", "missing"])],
        split=TrainTestConfig(test_size=0.34, random_state=0),
        model=ModelType.logistic_regression,
    )

    resp = asyncio.run(pipeline_service.run_pipeline(req))
    assert any("Skipped non-numeric or missing columns" in w for w in resp.warnings)
    assert resp.accuracy is not None


# 5) Pipeline: returns top-k feature importances (<= 15) when available

def test_pipeline_feature_importances_present_and_limited():
    df = pd.DataFrame(
        {
            **{f"f{i}": np.random.randn(60) for i in range(20)},
            "target": [0, 1] * 30,
        }
    )
    dataset_id = "dataset-feature-importance"
    dataset_service._dataset_store[dataset_id] = df

    req = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=[col for col in df.columns if col != "target"],
        preprocess=[PreprocessStep(step=PreprocessType.normalize)],
        split=TrainTestConfig(test_size=0.25, random_state=1),
        model=ModelType.logistic_regression,
    )

    resp = asyncio.run(pipeline_service.run_pipeline(req))
    assert resp.feature_importances is not None
    assert len(resp.feature_importances) <= 15
    assert all("name" in fi.model_dump() and "importance" in fi.model_dump() for fi in resp.feature_importances)
