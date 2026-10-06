from app.modules.predictions.ml import _train, demo_samples, evaluate, predict
from app.modules.predictions.schemas import PredictionCreate


def test_training_model_returns_valid_probability():
    model = _train()
    sample = demo_samples()[0]
    data = PredictionCreate(features=sample["features"])
    probability = predict(model, data)
    assert 0 <= probability <= 1


def test_evaluate_returns_holdout_metrics():
    metrics = evaluate()
    assert metrics["accuracy"] > 0.9
    assert 0 <= metrics["roc_auc"] <= 1
    assert metrics["roc_auc"] > 0.9
