"""Deterministic approval and risk decision boundary.

This module does not execute actions, call external services, or trust
agent-generated approval claims. It only classifies the request and returns
a safe decision result.
"""

from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    """Supported risk levels for requested actions."""

    LOW = "low"
    HIGH = "high"


class DecisionStatus(str, Enum):
    """Final decision status returned by the boundary."""

    ALLOWED = "allowed"
    REQUIRES_APPROVAL = "requires_approval"
    REJECTED = "rejected"

class SupportedAction(str, Enum):
    """Actions supported by the decision boundary."""

    READ_STATUS = "read_status"
    CREATE_PLAN = "create_plan"
    PROPOSE_CHANGE = "propose_change"

@dataclass(frozen=True)
class ActionRequest:
    """Input request for the decision boundary."""

    action: str
    risk_level: RiskLevel
    human_approved: bool = False
    agent_claimed_approval: bool = False


@dataclass(frozen=True)
class DecisionResult:
    """Deterministic decision result with minimal audit context."""

    status: DecisionStatus
    reason: str
    action: str | None = None
    risk_level: RiskLevel | None = None
    approval_required: bool = False

    def to_dict(self) -> dict[str, str | bool | None]:
        """Return a stable dictionary representation for audit and tests."""

        return {
            "status": self.status.value,
            "reason": self.reason,
            "action": self.action,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "approval_required": self.approval_required,
        }

SUPPORTED_ACTIONS = frozenset(action.value for action in SupportedAction)




def is_valid_action_request(request: ActionRequest | None) -> bool:
    """Return whether the request is structurally valid.

    This validation is intentionally small and deterministic.
    It rejects missing requests, empty actions, unsupported actions,
    and non-boolean approval flags before decision handling.
    """

    if request is None:
        return False

    if not isinstance(request.action, str) or not request.action.strip():
        return False

    if request.action not in SUPPORTED_ACTIONS:
        return False

    if not isinstance(request.human_approved, bool):
        return False

    if not isinstance(request.agent_claimed_approval, bool):
        return False

    return True


def decide_action(request: ActionRequest | None) -> DecisionResult:
    """Return a deterministic decision for a requested action."""

    if not is_valid_action_request(request):
        return DecisionResult(
            status=DecisionStatus.REJECTED,
            reason="invalid_request",
        )

    if request.risk_level == RiskLevel.HIGH and not request.human_approved:
        return DecisionResult(
            status=DecisionStatus.REQUIRES_APPROVAL,
            reason="human_approval_required",
            action=request.action,
            risk_level=request.risk_level,
            approval_required=True,
        )

    if request.risk_level == RiskLevel.HIGH and request.human_approved:
        return DecisionResult(
            status=DecisionStatus.ALLOWED,
            reason="human_approval_verified",
            action=request.action,
            risk_level=request.risk_level,
            approval_required=True,
        )

    if request.risk_level == RiskLevel.LOW:
        return DecisionResult(
            status=DecisionStatus.ALLOWED,
            reason="low_risk_action",
            action=request.action,
            risk_level=request.risk_level,
            approval_required=False,
        )

    return DecisionResult(
        status=DecisionStatus.REJECTED,
        reason="unrecognized_risk_level",
        action=request.action,
        risk_level=request.risk_level,
        approval_required=True,
    )

    def to_dict(self) -> dict[str, str | bool | None]:
        """Return a stable dictionary representation for audit and tests."""

        return {
            "status": self.status.value,
            "reason": self.reason,
            "action": self.action,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "approval_required": self.approval_required,
        }
