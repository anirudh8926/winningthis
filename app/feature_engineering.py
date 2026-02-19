"""Build ordered numpy feature vector for credit scoring model."""

import numpy as np
from typing import Any


# Canonical feature order for training and inference
FEATURE_ORDER = [
    "monthly_income",
    "income_stability",
    "rent_payment_consistency",
    "utility_payment_rate",
    "savings_ratio",
    "transaction_volume",
    "missed_payments",
    "gpa",
]


def build_feature_vector(
    monthly_income: float,
    income_stability: float,
    rent_payment_consistency: float,
    utility_payment_rate: float,
    savings_ratio: float,
    transaction_volume: int,
    missed_payments: int,
    gpa: float = 0.0,
) -> np.ndarray:
    """
    Build a 1D numpy feature array in fixed order for the model.

    Returns:
        np.ndarray: shape (8,) float64, same order as FEATURE_ORDER.
    """
    features = np.array(
        [
            float(monthly_income),
            float(income_stability),
            float(rent_payment_consistency),
            float(utility_payment_rate),
            float(savings_ratio),
            float(transaction_volume),
            float(missed_payments),
            float(gpa),
        ],
        dtype=np.float64,
    )
    return features.reshape(1, -1)


def build_feature_vector_from_record(record: dict[str, Any]) -> np.ndarray:
    """
    Build feature vector from a dict (e.g. request body or DataFrame row).
    Uses default gpa=0.0 if missing.
    """
    return build_feature_vector(
        monthly_income=record["monthly_income"],
        income_stability=record["income_stability"],
        rent_payment_consistency=record["rent_payment_consistency"],
        utility_payment_rate=record["utility_payment_rate"],
        savings_ratio=record["savings_ratio"],
        transaction_volume=int(record["transaction_volume"]),
        missed_payments=int(record["missed_payments"]),
        gpa=float(record.get("gpa", 0.0)),
    )
