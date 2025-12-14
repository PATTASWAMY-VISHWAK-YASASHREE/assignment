import pandas as pd

from app.services import dataset_service


def _store_dataset(df: pd.DataFrame) -> str:
    dataset_id = "artifact-dataset"
    dataset_service._dataset_store[dataset_id] = df
    return dataset_id


def test_pipeline_run_returns_model_and_allows_download(client):
    df = pd.DataFrame(
        {
            "f1": [1, 2, 3, 4, 5, 6, 7, 8],
            "f2": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "target": [0, 1, 0, 1, 0, 1, 0, 1],
        }
    )
    dataset_id = _store_dataset(df)

    payload = {
        "dataset_id": dataset_id,
        "target_column": "target",
        "feature_columns": ["f1", "f2"],
        "preprocess": [],
        "split": {"test_size": 0.25, "random_state": 0},
        "model": "logistic_regression",
        "drop_rare_classes": False,
    }

    response = client.post("/api/pipeline/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"]
    assert data["model_download_path"]

    download_resp = client.get(data["model_download_path"])
    assert download_resp.status_code == 200
    assert download_resp.headers["content-type"].startswith("application/octet-stream")
    assert len(download_resp.content) > 0


def test_predict_endpoint_uses_trained_model(client):
    df = pd.DataFrame(
        {
            "f1": [1, 2, 3, 4, 5, 6, 7, 8],
            "f2": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "target": [0, 1, 0, 1, 0, 1, 0, 1],
        }
    )
    dataset_id = _store_dataset(df)

    payload = {
        "dataset_id": dataset_id,
        "target_column": "target",
        "feature_columns": ["f1", "f2"],
        "preprocess": [],
        "split": {"test_size": 0.25, "random_state": 0},
        "model": "logistic_regression",
        "drop_rare_classes": False,
    }

    run_resp = client.post("/api/pipeline/run", json=payload)
    assert run_resp.status_code == 200
    model_id = run_resp.json()["model_id"]

    predict_payload = {"model_id": model_id, "records": [{"f1": 1.5, "f2": 0.25}]}
    predict_resp = client.post("/api/pipeline/predict", json=predict_payload)

    assert predict_resp.status_code == 200
    preds = predict_resp.json()["predictions"]
    assert isinstance(preds, list)
    assert len(preds) == 1
