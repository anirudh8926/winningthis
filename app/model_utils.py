"""Convert repayment probability to alternative credit score (300–900)."""

from typing import Union


def probability_to_score(probability: Union[float, int]) -> int:
    """
    Map repayment probability to alternative credit score.

    score = 300 + (probability * 600), clamped to [300, 900].

    Args:
        probability: Repayment probability in [0, 1].

    Returns:
        Integer score in range 300–900.
    """
    p = float(probability)
    score = 300.0 + (p * 600.0)
    return int(max(300, min(900, round(score))))
