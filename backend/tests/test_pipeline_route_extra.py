import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.pipeline import router
from app.schemas.pipeline import (
    PipelineRunRequest,
    PipelineRunResponse,
    ConfusionMatrix,
    ModelType,
    FeatureImportance,
    PredictRequest,
    PredictResponse,
)


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture()
def client(app):
    return TestClient(app)


@pytest.fixture()
def valid_request():
    return {
        "dataset_id": "ds-123",
        "target_column": "label",
        "feature_columns": ["f1", "f2"],
        "preprocess": [],
        "split": {"test_size": 0.2, "random_state": 42},
        "model": ModelType.logistic_regression.value,
    }


@pytest.fixture()
def sample_response():
    return PipelineRunResponse(
        status="success",
        accuracy=0.9,
        model_type=ModelType.logistic_regression,
        confusion_matrix=ConfusionMatrix(labels=[0, 1], matrix=[[5, 1], [0, 4]]),
        feature_importances=[FeatureImportance(name="f1", importance=0.7)],
        warnings=[],
    )


class TestPipelineRoute:
    @patch("app.api.routes.pipeline.pipeline_service.run_pipeline", new_callable=AsyncMock)
    def test_run_pipeline_success(self, mock_run, client, valid_request, sample_response):
        mock_run.return_value = sample_response

        resp = client.post("/pipeline/run", json=valid_request)

        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        assert body["model_type"] == ModelType.logistic_regression.value
        mock_run.assert_awaited_once()
        called_payload = mock_run.call_args[0][0]
        assert isinstance(called_payload, PipelineRunRequest)
        assert called_payload.dataset_id == "ds-123"

    @patch("app.api.routes.pipeline.pipeline_service.run_pipeline", new_callable=AsyncMock)
    def test_run_pipeline_value_error_returns_400(self, mock_run, client, valid_request):
        mock_run.side_effect = ValueError("bad things")

        resp = client.post("/pipeline/run", json=valid_request)

        assert resp.status_code == 400
        assert "bad things" in resp.json()["detail"]

    @patch("app.api.routes.pipeline.pipeline_service.run_pipeline", new_callable=AsyncMock)
    def test_run_pipeline_unexpected_returns_500(self, mock_run, client, valid_request):
        mock_run.side_effect = RuntimeError("boom")

        resp = client.post("/pipeline/run", json=valid_request)

        assert resp.status_code == 500
        assert "Pipeline execution failed" in resp.json()["detail"]

    def test_run_pipeline_missing_body_422(self, client):
        resp = client.post("/pipeline/run")
        assert resp.status_code == 422

    def test_run_pipeline_invalid_model_enum_422(self, client, valid_request):
        bad = {**valid_request, "model": "not-a-model"}
        resp = client.post("/pipeline/run", json=bad)
        assert resp.status_code == 422


class TestPipelinePredictRoute:
    @patch("app.api.routes.pipeline.pipeline_service.predict", new_callable=AsyncMock)
    def test_predict_success(self, mock_predict, client):
        payload = {"model_id": "model-123", "records": [{"f1": 1, "f2": 2}]}
        expected_response = PredictResponse(predictions=[0])
        mock_predict.return_value = expected_response

        resp = client.post("/pipeline/predict", json=payload)

        assert resp.status_code == 200
        assert resp.json() == {"predictions": [0]}
        mock_predict.assert_awaited_once_with("model-123", [{"f1": 1, "f2": 2}])

    @patch("app.api.routes.pipeline.pipeline_service.predict", new_callable=AsyncMock)
    def test_predict_value_error_returns_400(self, mock_predict, client):
        payload = {"model_id": "model-123", "records": [{"f1": 1, "f2": 2}]}
        mock_predict.side_effect = ValueError("Invalid input")

        resp = client.post("/pipeline/predict", json=payload)

        assert resp.status_code == 400
        assert "Invalid input" in resp.json()["detail"]

    @patch("app.api.routes.pipeline.pipeline_service.predict", new_callable=AsyncMock)
    def test_predict_unexpected_returns_500(self, mock_predict, client):
        payload = {"model_id": "model-123", "records": [{"f1": 1, "f2": 2}]}
        mock_predict.side_effect = RuntimeError("Unexpected error")

        resp = client.post("/pipeline/predict", json=payload)

        assert resp.status_code == 500
        assert "Prediction failed: Unexpected error" in resp.json()["detail"]

    def test_predict_missing_body_422(self, client):
        resp = client.post("/pipeline/predict")
        assert resp.status_code == 422
