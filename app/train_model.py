"""
Generate synthetic financial data and train the credit scoring model.
Saves training_data.csv and credit_model.pkl.
"""

import numpy as np
import pandas as pd
from pathlib import Path

from feature_engineering import FEATURE_ORDER
from model import train_and_save

RANDOM_SEED = 42
N_SAMPLES = 1200
DATA_PATH = Path(__file__).resolve().parent / "training_data.csv"


def generate_synthetic_data(n: int = N_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate synthetic financial records with logical correlations:
    higher stability / consistency / savings => lower default probability.
    """
    rng = np.random.default_rng(seed)

    # Base features: some correlated with default
    monthly_income = rng.uniform(1500, 12000, n)
    income_stability = rng.beta(2, 2, n)  # peak near 0.5, in [0,1]
    rent_payment_consistency = rng.beta(2, 2, n)
    utility_payment_rate = rng.beta(2, 2, n)
    savings_ratio = rng.beta(1.5, 3, n)  # skewed lower
    transaction_volume = rng.integers(10, 500, n)
    missed_payments = rng.integers(0, 8, n)
    gpa = rng.uniform(0, 4, n)

    # Default probability: lower when stability/consistency/savings higher
    # and when missed_payments lower and income higher
    p_default = (
        0.5
        - 0.15 * income_stability
        - 0.12 * rent_payment_consistency
        - 0.10 * utility_payment_rate
        - 0.12 * savings_ratio
        - 0.08 * np.clip(monthly_income / 12000, 0, 1)
        + 0.15 * np.clip(missed_payments / 8, 0, 1)
        - 0.03 * np.clip(gpa / 4, 0, 1)
    )
    p_default = np.clip(p_default, 0.05, 0.95)
    defaulted = (rng.uniform(0, 1, n) < p_default).astype(int)

    df = pd.DataFrame(
        {
            "monthly_income": monthly_income,
            "income_stability": income_stability,
            "rent_payment_consistency": rent_payment_consistency,
            "utility_payment_rate": utility_payment_rate,
            "savings_ratio": savings_ratio,
            "transaction_volume": transaction_volume,
            "missed_payments": missed_payments,
            "gpa": gpa,
            "defaulted": defaulted,
        }
    )
    return df


def main() -> None:
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    df.to_csv(DATA_PATH, index=False)
    print(f"Saved {len(df)} rows to {DATA_PATH}")

    X = df[FEATURE_ORDER].values.astype(np.float64)
    y = df["defaulted"].values

    print("Training Logistic Regression...")
    model, accuracy, path = train_and_save(X, y)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    main()
