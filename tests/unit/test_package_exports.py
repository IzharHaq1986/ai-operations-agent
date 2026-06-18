from ai_operations_agent import (
    ActionRequest,
    DecisionReason,
    DecisionResult,
    DecisionStatus,
    RiskLevel,
    SupportedAction,
    decide_action,
    is_valid_action_request,
    __version__,
   SUPPORTED_ACTIONS,
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


def test_package_version_is_available():
    assert __version__ == "0.1.0"

def test_supported_actions_export_is_available():
    assert len(SUPPORTED_ACTIONS) > 0
