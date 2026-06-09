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


@dataclass(frozen=True)
class ActionRequest:
    """Input request for the decision boundary."""

    action: str
    risk_level: RiskLevel
    human_approved: bool = False
    agent_claimed_approval: bool = False


@dataclass(frozen=True)
class DecisionResult:
    """Deterministic decision result."""

    status: DecisionStatus
    reason: str


SUPPORTED_ACTIONS = frozenset(
    {
        "read_status",
        "create_plan",
        "propose_change",
    }
)


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
        )

    if request.risk_level == RiskLevel.HIGH and request.human_approved:
        return DecisionResult(
            status=DecisionStatus.ALLOWED,
            reason="human_approval_verified",
        )

    if request.risk_level == RiskLevel.LOW:
        return DecisionResult(
            status=DecisionStatus.ALLOWED,
            reason="low_risk_action",
        )

    return DecisionResult(
        status=DecisionStatus.REJECTED,
        reason="unrecognized_risk_level",
    )
