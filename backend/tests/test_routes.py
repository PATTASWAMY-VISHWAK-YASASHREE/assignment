import pandas as pd

from app.schemas.pipeline import ModelType, PipelineRunRequest, PreprocessStep, PreprocessType, TrainTestConfig
from app.services import dataset_service


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_upload_dataset_empty_file_returns_400(client):
    resp = client.post("/api/datasets/upload", files={"file": ("empty.csv", b"", "text/csv")})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_upload_dataset_success(client, sample_csv_bytes):
    resp = client.post("/api/datasets/upload", files={"file": ("data.csv", sample_csv_bytes, "text/csv")})
    assert resp.status_code == 200
    body = resp.json()

    assert "dataset_id" in body
    assert body["rows"] == 6
    assert body["columns"] == 3
    assert set(body["column_names"]) == {"feature1", "feature2", "target"}

    stored = dataset_service.get_dataset(body["dataset_id"])
    assert isinstance(stored, pd.DataFrame)


def test_pipeline_run_via_api_success(client, sample_csv_bytes):
    upload = client.post("/api/datasets/upload", files={"file": ("data.csv", sample_csv_bytes, "text/csv")})
    dataset_id = upload.json()["dataset_id"]

    payload = PipelineRunRequest(
        dataset_id=dataset_id,
        target_column="target",
        feature_columns=["feature1", "feature2"],
        preprocess=[PreprocessStep(step=PreprocessType.normalize)],
        split=TrainTestConfig(test_size=0.34, random_state=0),
        model=ModelType.logistic_regression,
    ).model_dump()

    resp = client.post("/api/pipeline/run", json=payload)
    assert resp.status_code == 200
    body = resp.json()

    assert body["status"] == "success"
    assert "accuracy" in body
    assert body["confusion_matrix"]["labels"] == [0, 1]
    assert body["model_type"] == ModelType.logistic_regression.value

def test_pipeline_run_missing_target_returns_400(client, sample_csv_bytes):
    upload = client.post("/api/datasets/upload", files={"file": ("data.csv", sample_csv_bytes, "text/csv")})
    dataset_id = upload.json()["dataset_id"]

    payload = {
        "dataset_id": dataset_id,
        "target_column": "missing",
        "feature_columns": ["feature1", "feature2"],
        "preprocess": [],
        "split": {"test_size": 0.2, "random_state": 42},
        "model": ModelType.logistic_regression.value,
    }

    resp = client.post("/api/pipeline/run", json=payload)
    assert resp.status_code == 400
    assert "target column" in resp.json()["detail"].lower()
