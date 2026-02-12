import pytest
import pandas as pd
from unittest.mock import MagicMock
from app.services import pipeline_service
from app.schemas.pipeline import PipelineRunRequest, TrainTestConfig, ModelType, PreprocessStep

@pytest.mark.asyncio
async def test_predict_type_mismatch_fix():
    # 1. Setup Mock Dataset
    # feature1: even -> 1, odd -> 0
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5, 6],
        "target": [0, 1, 0, 1, 0, 1]
    })

    # Mock get_dataset to return our dataframe
    original_get_dataset = pipeline_service.dataset_service.get_dataset
    pipeline_service.dataset_service.get_dataset = MagicMock(return_value=df)

    try:
        # 2. Run Pipeline
        request = PipelineRunRequest(
            dataset_id="test-dataset",
            target_column="target",
            feature_columns=["feature1"],
            preprocess=[],
            split=TrainTestConfig(test_size=0.2, random_state=42),
            model=ModelType.logistic_regression
        )

        response = await pipeline_service.run_pipeline(request)
        model_id = response.model_id

        # 3. Predict with correct type (int) -> Should predict 1
        pred_correct = await pipeline_service.predict(model_id, [{"feature1": 4}])

        # 4. Predict with incorrect type (str) -> Should also predict 1 if fixed
        pred_string = await pipeline_service.predict(model_id, [{"feature1": "4"}])

        print(f"Prediction (int): {pred_correct.predictions}")
        print(f"Prediction (str): {pred_string.predictions}")

        assert pred_correct.predictions == [1], "Baseline prediction failed"
        assert pred_string.predictions == [1], "String input prediction failed (bug still exists)"
        assert pred_correct.predictions == pred_string.predictions

    finally:
        # Restore mock
        pipeline_service.dataset_service.get_dataset = original_get_dataset
