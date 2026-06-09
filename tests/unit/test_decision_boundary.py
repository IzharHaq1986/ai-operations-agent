from ai_operations_agent.decision_boundary import (
    ActionRequest,
    DecisionStatus,
    RiskLevel,
    decide_action,
)


def test_missing_request_is_rejected():
    result = decide_action(None)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == "invalid_request"


def test_unsupported_action_is_rejected():
    request = ActionRequest(
        action="deploy_to_production",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == "invalid_request"


def test_low_risk_supported_action_is_allowed():
    request = ActionRequest(
        action="read_status",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.ALLOWED
    assert result.reason == "low_risk_action"


def test_high_risk_action_requires_human_approval():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REQUIRES_APPROVAL
    assert result.reason == "human_approval_required"


def test_high_risk_action_is_allowed_with_human_approval():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
        human_approved=True,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.ALLOWED
    assert result.reason == "human_approval_verified"


def test_agent_claimed_approval_does_not_bypass_human_approval():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
        human_approved=False,
        agent_claimed_approval=True,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REQUIRES_APPROVAL
    assert result.reason == "human_approval_required"


def test_blank_action_is_rejected():
    request = ActionRequest(
        action=" ",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == "invalid_request"


def test_non_boolean_human_approval_is_rejected():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
        human_approved="yes",  # type: ignore[arg-type]
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == "invalid_request"


def test_non_boolean_agent_claimed_approval_is_rejected():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
        agent_claimed_approval="yes",  # type: ignore[arg-type]
    )

    result = decide_action(request)

    assert result.status == DecisionStatus.REJECTED
    assert result.reason == "invalid_request"


def test_low_risk_result_includes_audit_context():
    request = ActionRequest(
        action="read_status",
        risk_level=RiskLevel.LOW,
    )

    result = decide_action(request)

    assert result.action == "read_status"
    assert result.risk_level == RiskLevel.LOW
    assert result.approval_required is False


def test_high_risk_result_requires_approval_in_audit_context():
    request = ActionRequest(
        action="propose_change",
        risk_level=RiskLevel.HIGH,
    )

    result = decide_action(request)

    assert result.action == "propose_change"
    assert result.risk_level == RiskLevel.HIGH
    assert result.approval_required is True


def test_invalid_request_result_does_not_include_trusted_audit_context():
    result = decide_action(None)

    assert result.action is None
    assert result.risk_level is None
    assert result.approval_required is False
