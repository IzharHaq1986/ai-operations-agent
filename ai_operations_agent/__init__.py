"""Public package exports for AI Operations Agent."""

__version__ = "0.1.0"

from ai_operations_agent.failure_summary import FailureSummary

from ai_operations_agent.decision_boundary import (
    ActionRequest,
    DecisionReason,
    DecisionResult,
    DecisionStatus,
    RiskLevel,
    SupportedAction,
    decide_action,
    is_valid_action_request,
    SUPPORTED_ACTIONS,
)

from ai_operations_agent.failure_classifier import (
    FailureCategory,
    FailureClassification,
    FailureInput,
    FailureReason,
    FailureSeverity,
    FailureStatus,
    classify_failure,
    is_valid_failure_input,
)


__all__ = [
    "ActionRequest",
    "DecisionReason",
    "DecisionResult",
    "DecisionStatus",
    "RiskLevel",
    "SupportedAction",
    "decide_action",
    "is_valid_action_request",
    "__version__",
    "SUPPORTED_ACTIONS",
    "FailureCategory",
    "FailureClassification",
    "FailureInput",
    "FailureReason",
    "FailureSeverity",
    "FailureStatus",
    "classify_failure",
    "is_valid_failure_input",
    "FailureSummary"
]


