"""Deterministic failure summary boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureSummary:
    """Structured operator-facing summary for a classified failure."""

    category: str
    severity: str
    reason: str
    review_required: bool
