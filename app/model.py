"""
Credit scoring model: StandardScaler + LogisticRegression pipeline,
wrapped in CalibratedClassifierCV for well-calibrated probability outputs.

Calibration ensures that predict_proba(X) ≈ true posterior P(default | X),
which is critical for credit score mapping and risk thresholds.
"""

import joblib
import numpy as np
from pathlib import Path
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from typing import Tuple

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "credit_model.pkl"


def _build_base_pipeline() -> Pipeline:
    """StandardScaler + LogisticRegression pipeline (uncalibrated)."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            max_iter=5000,
            random_state=42,
            solver="lbfgs",
            class_weight="balanced",   # upweight default class to improve recall
        )),
    ])


def train_model(X: np.ndarray, y: np.ndarray) -> CalibratedClassifierCV:
    """
    Train a calibrated credit scoring model.

    Architecture:
        CalibratedClassifierCV(
            estimator = Pipeline(StandardScaler -> LogisticRegression),
            method    = 'sigmoid'   # Platt scaling
            cv        = 5
        )

    Platt scaling fits a sigmoid on hold-out fold predictions to align
    predicted probabilities with actual default rates.

    Args:
        X: Feature matrix, shape (n_samples, n_features).
        y: Binary labels (0 = default, 1 = repay), shape (n_samples,).

    Returns:
        Fitted CalibratedClassifierCV.
    """
    base = _build_base_pipeline()
    calibrated = CalibratedClassifierCV(
        estimator=base,
        method="sigmoid",   # Platt scaling
        cv=5,
    )
    calibrated.fit(X, y)
    return calibrated


def save_model(model: CalibratedClassifierCV, path=None) -> Path:
    """Save the calibrated model with joblib."""
    out_path = Path(path) if path is not None else DEFAULT_MODEL_PATH
    out_path = out_path.resolve()
    joblib.dump(model, out_path)
    return out_path


def load_model(path=None) -> CalibratedClassifierCV:
    """Load a persisted calibrated model from disk."""
    p = Path(path) if path is not None else DEFAULT_MODEL_PATH
    p = p.resolve()
    if not p.is_file():
        raise FileNotFoundError(f"Model file not found: {p}")
    return joblib.load(p)


def evaluate_calibration(
    model: CalibratedClassifierCV,
    X: np.ndarray,
    y: np.ndarray,
    n_bins: int = 10,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute calibration curve (fraction of positives vs mean predicted prob).

    Returns:
        (fraction_of_positives, mean_predicted_probability)
    """
    proba = model.predict_proba(X)[:, 1]
    frac_pos, mean_prob = calibration_curve(y, proba, n_bins=n_bins)
    return frac_pos, mean_prob


def evaluate_accuracy(model: CalibratedClassifierCV, X: np.ndarray, y: np.ndarray) -> float:
    """Compute accuracy on (X, y)."""
    return float(model.score(X, y))


def train_and_save(
    X: np.ndarray,
    y: np.ndarray,
    model_path=None,
) -> Tuple[CalibratedClassifierCV, float, Path]:
    """Train, evaluate, save, and return (model, accuracy, path)."""
    model    = train_model(X, y)
    accuracy = evaluate_accuracy(model, X, y)
    print(f"Model accuracy: {accuracy:.4f}")
    path = save_model(model, path=model_path)
    return model, accuracy, path
