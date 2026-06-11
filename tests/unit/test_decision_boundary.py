from ai_operations_agent.decision_boundary import (
    ActionRequest,
    DecisionReason,
    DecisionStatus,
    RiskLevel,
    SUPPORTED_ACTIONS,
    SupportedAction,
    decide_action,
)


def test_missing_request_is_rejected():
    result = decide_action(None)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value


def test_unsupported_action_is_rejected():
    request = ActionRequest(
        action="deploy_to_production",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value


def test_low_risk_supported_action_is_allowed():
    request = ActionRequest(
        action=SupportedAction.READ_STATUS.value,
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.ALLOWED
    assert result.reason == DecisionReason.LOW_RISK_ACTION.value


def test_high_risk_action_requires_human_approval():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REQUIRES_APPROVAL
    assert result.reason == DecisionReason.HUMAN_APPROVAL_REQUIRED.value


def test_high_risk_action_is_allowed_with_human_approval():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
        human_approved=True,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.ALLOWED
    assert result.reason == DecisionReason.HUMAN_APPROVAL_VERIFIED.value


def test_agent_claimed_approval_does_not_bypass_human_approval():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
        human_approved=False,
        agent_claimed_approval=True,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REQUIRES_APPROVAL
    assert result.reason == DecisionReason.HUMAN_APPROVAL_REQUIRED.value


def test_blank_action_is_rejected():
    request = ActionRequest(
        action=" ",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value


def test_non_boolean_human_approval_is_rejected():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
        human_approved="yes",  # type: ignore[arg-type]
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value


def test_non_boolean_agent_claimed_approval_is_rejected():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
        agent_claimed_approval="yes",  # type: ignore[arg-type]
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value


def test_low_risk_result_includes_audit_context():
    request = ActionRequest(
        action=SupportedAction.READ_STATUS.value,
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.action == SupportedAction.READ_STATUS.value
    assert result.risk_level == RiskLevel.LOW
    assert result.approval_required is False


def test_high_risk_result_requires_approval_in_audit_context():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
    )

    result = decide_action(request)

    assert result.action == SupportedAction.PROPOSE_CHANGE.value
    assert result.risk_level == RiskLevel.HIGH
    assert result.approval_required is True


def test_invalid_request_result_does_not_include_trusted_audit_context():
    result = decide_action(None)

    assert result.action is None
    assert result.risk_level is None
    assert result.approval_required is False


def test_decision_result_serializes_low_risk_action():
    request = ActionRequest(
        action=SupportedAction.READ_STATUS.value,
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.to_dict() == {
        "status": DecisionStatus.ALLOWED.value,
        "reason": DecisionReason.LOW_RISK_ACTION.value,
        "action": SupportedAction.READ_STATUS.value,
        "risk_level": RiskLevel.LOW.value,
        "approval_required": False,
    }


def test_decision_result_serializes_high_risk_approval_required_action():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
    )

    result = decide_action(request)

    assert result.to_dict() == {
        "status": DecisionStatus.REQUIRES_APPROVAL.value,
        "reason": DecisionReason.HUMAN_APPROVAL_REQUIRED.value,
        "action": SupportedAction.PROPOSE_CHANGE.value,
        "risk_level": RiskLevel.HIGH.value,
        "approval_required": True,
    }


def test_decision_result_serializes_invalid_request_without_trusted_context():
    result = decide_action(None)

    assert result.to_dict() == {
        "status": DecisionStatus.REJECTED.value,
        "reason": DecisionReason.INVALID_REQUEST.value,
        "action": None,
        "risk_level": None,
        "approval_required": False,
    }


def test_supported_action_constants_match_allowed_actions():
    assert SUPPORTED_ACTIONS == {
        SupportedAction.READ_STATUS.value,
        SupportedAction.CREATE_PLAN.value,
        SupportedAction.PROPOSE_CHANGE.value,
    }


def test_decision_reason_constants_match_expected_values():
    assert DecisionReason.INVALID_REQUEST.value == "invalid_request"
    assert DecisionReason.HUMAN_APPROVAL_REQUIRED.value == "human_approval_required"
    assert DecisionReason.HUMAN_APPROVAL_VERIFIED.value == "human_approval_verified"
    assert DecisionReason.LOW_RISK_ACTION.value == "low_risk_action"
    assert DecisionReason.UNRECOGNIZED_RISK_LEVEL.value == "unrecognized_risk_level"


def test_invalid_risk_level_is_rejected():
    request = ActionRequest(
        action=SupportedAction.READ_STATUS.value,
        risk_level="medium",  # type: ignore[arg-type]
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == DecisionReason.INVALID_REQUEST.value
    assert result.action is None
    assert result.risk_level is None
    assert result.approval_required is False


def test_decision_result_serializes_approved_high_risk_action():
    request = ActionRequest(
        action=SupportedAction.PROPOSE_CHANGE.value,
        risk_level=RiskLevel.HIGH,
        human_approved=True,
    )

    result = decide_action(request)

    assert result.to_dict() == {
        "status": DecisionStatus.ALLOWED.value,
        "reason": DecisionReason.HUMAN_APPROVAL_VERIFIED.value,
        "action": SupportedAction.PROPOSE_CHANGE.value,
        "risk_level": RiskLevel.HIGH.value,
        "approval_required": True,
    }
