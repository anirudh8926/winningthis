"""
Credit scoring model: train LogisticRegression and persist with joblib.
"""

import joblib
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from typing import Tuple

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "credit_model.pkl"


def train_model(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    """
    Train a LogisticRegression classifier on feature matrix X and labels y.

    Args:
        X: Feature matrix, shape (n_samples, n_features).
        y: Binary labels (0/1), shape (n_samples,).

    Returns:
        Fitted LogisticRegression model.
    """
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        solver="lbfgs",
    )
    model.fit(X, y)
    return model


def save_model(model: LogisticRegression, path: Path | str | None = None) -> Path:
    """
    Save the trained model to disk with joblib.

    Args:
        model: Fitted LogisticRegression model.
        path: File path. Defaults to credit_model.pkl next to this file.

    Returns:
        Resolved path where the model was saved.
    """
    out_path = Path(path) if path is not None else DEFAULT_MODEL_PATH
    out_path = out_path.resolve()
    joblib.dump(model, out_path)
    return out_path


def load_model(path: Path | str | None = None) -> LogisticRegression:
    """
    Load a persisted LogisticRegression model from disk.

    Args:
        path: File path. Defaults to credit_model.pkl next to this file.

    Returns:
        Loaded LogisticRegression model.

    Raises:
        FileNotFoundError: If the model file does not exist.
    """
    p = Path(path) if path is not None else DEFAULT_MODEL_PATH
    p = p.resolve()
    if not p.is_file():
        raise FileNotFoundError(f"Model file not found: {p}")
    return joblib.load(p)


def predict_proba(model: LogisticRegression, X: np.ndarray) -> np.ndarray:
    """
    Predict class probabilities for samples.

    Args:
        model: Fitted LogisticRegression model.
        X: Feature matrix, shape (n_samples, n_features).

    Returns:
        Array of shape (n_samples,) with probability of class 1 (repayment).
    """
    return model.predict_proba(X)[:, 1]


def evaluate_accuracy(model: LogisticRegression, X: np.ndarray, y: np.ndarray) -> float:
    """
    Compute accuracy of the model on (X, y).

    Returns:
        Accuracy in [0, 1].
    """
    return float(model.score(X, y))


def train_and_save(
    X: np.ndarray,
    y: np.ndarray,
    model_path: Path | str | None = None,
) -> Tuple[LogisticRegression, float, Path]:
    """
    Train model, print accuracy, save with joblib, and return model, accuracy, path.

    Args:
        X: Feature matrix.
        y: Labels.
        model_path: Where to save the model.

    Returns:
        (model, accuracy, path).
    """
    model = train_model(X, y)
    accuracy = evaluate_accuracy(model, X, y)
    print(f"Model accuracy: {accuracy:.4f}")
    path = save_model(model, path=model_path)
    return model, accuracy, path
