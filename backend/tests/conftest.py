import sys
from io import BytesIO
from pathlib import Path
from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Ensure backend package is importable when running from workspace root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import create_app  # noqa: E402
from app.services import dataset_service  # noqa: E402


@pytest.fixture(autouse=True)
def reset_dataset_store() -> None:
    """Clear the in-memory dataset store between tests to avoid cross-test leakage."""
    dataset_service._dataset_store.clear()


@pytest.fixture()
def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "target": [0, 1, 0, 1, 0, 1],
        }
    )


@pytest.fixture()
def sample_csv_bytes(sample_dataframe: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    sample_dataframe.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer.read()


@pytest.fixture()
def app():
    return create_app()


@pytest.fixture()
def client(app) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
