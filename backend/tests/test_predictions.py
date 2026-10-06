import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_session
from app.main import app
from app.modules.predictions.ml import _dataset

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
def client():
    Base.metadata.create_all(engine)

    def override_session():
        with TestingSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_wdbc_prediction_and_history(client):
    sample = client.get("/api/v1/predictions/samples").json()[0]
    response = client.post("/api/v1/predictions?sample_name=Тестовый&reference_class=malignant", json={"features": sample["features"]})
    assert response.status_code == 201
    prediction = response.json()
    assert prediction["reference_class"] == "malignant"
    assert prediction["predicted_class"] in {"benign", "malignant"}
    assert 0 <= prediction["malignant_probability"] <= 1
    assert "не медицинский диагноз" in prediction["disclaimer"]
    assert client.get("/api/v1/predictions").json()[0]["id"] == prediction["id"]


def test_rejects_missing_wdbc_features(client):
    response = client.post("/api/v1/predictions", json={"features": {"mean radius": 12.0}})
    assert response.status_code == 422


def test_metrics_are_from_holdout(client):
    payload = client.get("/api/v1/predictions/metrics").json()
    assert payload["sample_count"] == 569
    assert payload["train_fraction"] == 0.8
    assert 0 <= payload["metrics"]["roc_auc"] <= 1


def test_dataset_target_is_explicit():
    _, labels, _, dataset = _dataset()
    assert labels.sum() == (dataset.target == 0).sum()
