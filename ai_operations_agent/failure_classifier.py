"""Deterministic failure classification boundary.

This module classifies explicitly provided structured failure text.
It does not ingest logs, call external services, execute tools, or perform
remediation actions.
"""

from dataclasses import dataclass
from enum import Enum


class FailureCategory(str, Enum):
    """Supported failure categories."""

    DEPENDENCY = "dependency"
    TEST = "test"
    LINT = "lint"
    CONFIGURATION = "configuration"
    UNKNOWN = "unknown"


class FailureSeverity(str, Enum):
    """Supported failure severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class FailureStatus(str, Enum):
    """Classification status values."""

    CLASSIFIED = "classified"
    REJECTED = "rejected"


class FailureReason(str, Enum):
    """Stable reason codes for failure classification."""

    CLASSIFIED_DEPENDENCY_FAILURE = "classified_dependency_failure"
    CLASSIFIED_TEST_FAILURE = "classified_test_failure"
    CLASSIFIED_LINT_FAILURE = "classified_lint_failure"
    CLASSIFIED_CONFIGURATION_FAILURE = "classified_configuration_failure"
    CLASSIFIED_UNKNOWN_FAILURE = "classified_unknown_failure"
    INVALID_FAILURE_INPUT = "invalid_failure_input"


@dataclass(frozen=True)
class FailureInput:
    """Structured input for deterministic failure classification."""

    message: str


@dataclass(frozen=True)
class FailureClassification:
    """Deterministic classification result."""

    status: FailureStatus
    reason: str
    category: FailureCategory
    severity: FailureSeverity
    review_required: bool

    def to_dict(self) -> dict[str, str | bool]:
        """Return a stable dictionary representation for audit and tests."""

        return {
            "status": self.status.value,
            "reason": self.reason,
            "category": self.category.value,
            "severity": self.severity.value,
            "review_required": self.review_required,
        }


def is_valid_failure_input(failure_input: FailureInput | None) -> bool:
    """Return whether the failure input is structurally valid."""

    if failure_input is None:
        return False

    if not isinstance(failure_input.message, str):
        return False

    if not failure_input.message.strip():
        return False

    return True


def classify_failure(failure_input: FailureInput | None) -> FailureClassification:
    """Classify explicitly provided structured failure input."""

    if not is_valid_failure_input(failure_input):
        return FailureClassification(
            status=FailureStatus.REJECTED,
            reason=FailureReason.INVALID_FAILURE_INPUT.value,
            category=FailureCategory.UNKNOWN,
            severity=FailureSeverity.UNKNOWN,
            review_required=True,
        )

    message = failure_input.message.lower()

    if "dependency" in message or "package" in message or "importerror" in message:
        return FailureClassification(
            status=FailureStatus.CLASSIFIED,
            reason=FailureReason.CLASSIFIED_DEPENDENCY_FAILURE.value,
            category=FailureCategory.DEPENDENCY,
            severity=FailureSeverity.MEDIUM,
            review_required=True,
        )

    if "test failed" in message or "assertionerror" in message or "pytest" in message:
        return FailureClassification(
            status=FailureStatus.CLASSIFIED,
            reason=FailureReason.CLASSIFIED_TEST_FAILURE.value,
            category=FailureCategory.TEST,
            severity=FailureSeverity.MEDIUM,
            review_required=True,
        )

    if "ruff" in message or "lint" in message or "format" in message:
        return FailureClassification(
            status=FailureStatus.CLASSIFIED,
            reason=FailureReason.CLASSIFIED_LINT_FAILURE.value,
            category=FailureCategory.LINT,
            severity=FailureSeverity.LOW,
            review_required=False,
        )

    if "yaml" in message or "config" in message or "configuration" in message:
        return FailureClassification(
            status=FailureStatus.CLASSIFIED,
            reason=FailureReason.CLASSIFIED_CONFIGURATION_FAILURE.value,
            category=FailureCategory.CONFIGURATION,
            severity=FailureSeverity.HIGH,
            review_required=True,
        )

    return FailureClassification(
        status=FailureStatus.CLASSIFIED,
        reason=FailureReason.CLASSIFIED_UNKNOWN_FAILURE.value,
        category=FailureCategory.UNKNOWN,
        severity=FailureSeverity.UNKNOWN,
        review_required=True,
    )
