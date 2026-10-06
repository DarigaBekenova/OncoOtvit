from sqlalchemy import select
from sqlalchemy.orm import Session

from .ml import MODEL_VERSION, demo_samples, evaluate, load_model, predict
from .models import Prediction
from .schemas import PredictionCreate

_model = None


def create_prediction(
    session: Session, data: PredictionCreate, sample_name: str, reference_class: str
) -> Prediction:
    global _model
    if _model is None:
        _model = load_model()
    probability = predict(_model, data)
    predicted_class = "malignant" if probability >= 0.5 else "benign"
    result = Prediction(
        sample_name=sample_name,
        reference_class=reference_class,
        predicted_class=predicted_class,
        malignant_probability=probability,
        model_version=MODEL_VERSION,
    )
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def list_predictions(session: Session, limit: int = 50) -> list[Prediction]:
    return list(session.scalars(select(Prediction).order_by(Prediction.id.desc()).limit(limit)))


def get_demo_samples():
    return demo_samples()


def get_model_metrics():
    metrics = evaluate()
    return {
        "dataset": "Breast Cancer Wisconsin Diagnostic (WDBC)",
        "sample_count": 569,
        "train_fraction": 0.8,
        "metrics": metrics,
    }
