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


def decide_action(request: ActionRequest | None) -> DecisionResult:
    """Return a deterministic decision for a requested action."""

    if request is None:
        return DecisionResult(
            status=DecisionStatus.REJECTED,
            reason="missing_request",
        )

    if not request.action or request.action not in SUPPORTED_ACTIONS:
        return DecisionResult(
            status=DecisionStatus.REJECTED,
            reason="unsupported_action",
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
