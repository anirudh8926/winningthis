"""
FastAPI backend for alternative credit scoring.
POST /predict returns repayment_probability and alternative_credit_score (300–900).
"""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from feature_engineering import build_feature_vector_from_record
from model import load_model, DEFAULT_MODEL_PATH
from model_utils import probability_to_score

app = FastAPI(title="Alternative Credit Scoring API", version="1.0.0")

# Load model at startup (or on first predict)
_model = None


def get_model():
    global _model
    if _model is None:
        try:
            _model = load_model(DEFAULT_MODEL_PATH)
        except FileNotFoundError:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Run train_model.py to generate credit_model.pkl.",
            )
    return _model


class PredictRequest(BaseModel):
    monthly_income: float = Field(..., ge=0, description="Monthly income")
    income_stability: float = Field(..., ge=0, le=1, description="Income stability 0–1")
    rent_payment_consistency: float = Field(..., ge=0, le=1, description="Rent payment consistency 0–1")
    utility_payment_rate: float = Field(..., ge=0, le=1, description="Utility payment rate 0–1")
    savings_ratio: float = Field(..., ge=0, le=1, description="Savings ratio 0–1")
    transaction_volume: int = Field(..., ge=0, description="Transaction volume")
    missed_payments: int = Field(..., ge=0, description="Number of missed payments")
    gpa: float = Field(default=0.0, ge=0, le=4, description="GPA (optional)")


class PredictResponse(BaseModel):
    repayment_probability: float
    alternative_credit_score: int


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Alternative Credit Scoring API", "docs": "/docs"}


@app.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest) -> dict[str, Any]:
    """
    Predict repayment probability and alternative credit score (300–900).
    """
    try:
        model = get_model()
        record = body.model_dump()
        X = build_feature_vector_from_record(record)
        proba = float(model.predict_proba(X)[0, 0])  # P(repay) = P(no default) = class 0
        score = probability_to_score(proba)
        return {
            "repayment_probability": round(proba, 6),
            "alternative_credit_score": score,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
