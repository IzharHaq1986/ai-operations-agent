"""Deterministic failure summary boundary."""

from dataclasses import dataclass

from ai_operations_agent.failure_classifier import FailureClassification


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


def create_failure_summary(
    classification: FailureClassification,
) -> FailureSummary:
    """Create a deterministic summary from a failure classification."""

    return FailureSummary(
        category=classification.category.value,
        severity=classification.severity.value,
        reason=classification.reason,
        review_required=classification.review_required,
    )
