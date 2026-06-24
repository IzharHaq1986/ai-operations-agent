"""Deterministic failure summary boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureSummary:
    """Structured operator-facing summary for a classified failure."""

    category: str
    severity: str
    reason: str
    review_required: bool

    def to_dict(self) -> dict[str, str | bool]:
        """Return a stable dictionary representation of the failure summary."""

        return {
            "category": self.category,
            "severity": self.severity,
            "reason": self.reason,
            "review_required": self.review_required,
        }
