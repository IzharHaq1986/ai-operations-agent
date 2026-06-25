from ai_operations_agent import (
    SUPPORTED_ACTIONS,
    ActionRequest,
    DecisionReason,
    DecisionResult,
    DecisionStatus,
    FailureCategory,
    FailureClassification,
    FailureInput,
    FailureReason,
    FailureSeverity,
    FailureStatus,
    FailureSummary,
    RiskLevel,
    SupportedAction,
    __version__,
    classify_failure,
    create_failure_summary,
    decide_action,
    is_valid_action_request,
    is_valid_failure_classification,
    is_valid_failure_input,
)


def test_public_package_exports_are_available():
    assert ActionRequest is not None
    assert DecisionReason is not None
    assert DecisionResult is not None
    assert DecisionStatus is not None
    assert RiskLevel is not None
    assert SupportedAction is not None
    assert decide_action is not None
    assert is_valid_action_request is not None
    assert FailureCategory is not None
    assert FailureClassification is not None
    assert FailureInput is not None
    assert FailureReason is not None
    assert FailureSeverity is not None
    assert FailureStatus is not None
    assert classify_failure is not None
    assert is_valid_failure_input is not None


def test_package_version_is_available():
    assert __version__ == "0.1.0"


def test_supported_actions_export_is_available():
    assert len(SUPPORTED_ACTIONS) > 0


def test_failure_summary_type_is_exported():
    assert FailureSummary is not None


def test_failure_summary_helpers_are_exported():
    assert create_failure_summary is not None
    assert is_valid_failure_classification is not None
