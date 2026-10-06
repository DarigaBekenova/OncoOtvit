from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.predictions.ml import _dataset

_FEATURE_NAMES = _dataset()[2]


class PredictionCreate(BaseModel):
    features: dict[str, float]

    model_config = ConfigDict(extra="forbid")

    @field_validator("features")
    @classmethod
    def validate_features(cls, value: dict[str, float]) -> dict[str, float]:
        if set(value) != set(_FEATURE_NAMES):
            raise ValueError("Необходимо передать все 30 признаков WDBC")
        return value


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sample_name: str
    reference_class: str
    predicted_class: Literal["benign", "malignant"]
    malignant_probability: float = Field(ge=0, le=1)
    model_version: str
    created_at: datetime
    disclaimer: str = "Учебная классификация набора WDBC; не медицинский диагноз или рекомендация."


class DemoSample(BaseModel):
    id: int
    description: str
    features: dict[str, float]
    reference_class: Literal["benign", "malignant"]


class ModelMetrics(BaseModel):
    dataset: str
    sample_count: int
    train_fraction: float
    metrics: dict[str, float]
