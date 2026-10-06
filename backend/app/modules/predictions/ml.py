from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.core.config import settings

MODEL_VERSION = "wdbc-logistic-regression-1.0"
DATASET_NAME = "Breast Cancer Wisconsin Diagnostic (WDBC)"
RANDOM_STATE = 42


def _dataset() -> tuple[np.ndarray, np.ndarray, list[str], Any]:
    dataset = load_breast_cancer()
    features = dataset.data
    labels = (dataset.target == 0).astype(int)
    return features, labels, list(dataset.feature_names), dataset


def _split() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    features, labels, _, _ = _dataset()
    return train_test_split(
        features, labels, test_size=0.2, random_state=RANDOM_STATE, stratify=labels
    )


def _train() -> Pipeline:
    x_train, _, y_train, _ = _split()
    model = Pipeline(
        [("scaler", StandardScaler()), ("classifier", LogisticRegression(max_iter=2000))]
    )
    model.fit(x_train, y_train)
    return model


def evaluate() -> dict[str, float]:
    x_train, x_test, y_train, y_test = _split()
    model = Pipeline(
        [("scaler", StandardScaler()), ("classifier", LogisticRegression(max_iter=2000))]
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions)),
        "recall": float(recall_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
    }


def _is_current_model(model: object) -> bool:
    if not isinstance(model, Pipeline):
        return False
    steps = dict(model.steps)
    if set(steps) != {"scaler", "classifier"}:
        return False
    scaler = steps["scaler"]
    return isinstance(scaler, StandardScaler) and getattr(scaler, "n_features_in_", 30) == 30


def load_model() -> Pipeline:
    model_path = Path(settings.model_path)
    if model_path.exists():
        try:
            loaded = joblib.load(model_path)
        except (OSError, ValueError, EOFError):
            loaded = None
        if loaded is not None and _is_current_model(loaded):
            return loaded
    model = _train()
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return model


def predict(model: Pipeline, data: Any) -> float:
    _, _, feature_names, _ = _dataset()
    row = np.asarray([[data.features[name] for name in feature_names]])
    return float(model.predict_proba(row)[0, 1])


def demo_samples() -> list[dict[str, Any]]:
    _, x_test, _, y_test = _split()
    _, _, feature_names, _ = _dataset()
    indices = [0, 1, 2, 3]
    samples = []
    for sample_id, index in enumerate(indices, start=1):
        features = {name: float(value) for name, value in zip(feature_names, x_test[index], strict=True)}
        samples.append(
            {
                "id": sample_id,
                "description": f"Демонстрационный образец {sample_id}",
                "features": features,
                "reference_class": "malignant" if y_test[index] else "benign",
            }
        )
    return samples
