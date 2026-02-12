from fastapi.testclient import TestClient
from app.core.config import settings

def test_health_check_public(client: TestClient):
    # Health check should work even without auth
    client.headers.pop("X-API-Key", None)
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_upload_dataset_no_auth_fails(client: TestClient):
    client.headers.pop("X-API-Key", None)
    resp = client.post("/api/datasets/upload", files={"file": ("test.csv", b"test", "text/csv")})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Could not validate credentials"

def test_upload_dataset_wrong_auth_fails(client: TestClient):
    client.headers["X-API-Key"] = "wrong-key"
    resp = client.post("/api/datasets/upload", files={"file": ("test.csv", b"test", "text/csv")})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Could not validate credentials"

def test_pipeline_run_no_auth_fails(client: TestClient):
    client.headers.pop("X-API-Key", None)
    resp = client.post("/api/pipeline/run", json={})
    assert resp.status_code == 401
