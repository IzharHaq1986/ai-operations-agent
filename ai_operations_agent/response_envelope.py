"""Deterministic response envelope boundary."""

from dataclasses import dataclass

from ai_operations_agent.failure_summary import FailureSummary


@dataclass(frozen=True)
class ResponseEnvelope:
    """Stable response wrapper for trusted failure summaries."""

    status: str
    summary: FailureSummary

    def to_dict(self) -> dict[str, object]:
        """Return a stable dictionary representation of the response envelope."""

        return {
            "status": self.status,
            "summary": self.summary.to_dict(),
        }


def is_valid_response_summary(summary: object) -> bool:
    """Return whether a value is a valid response summary."""

    return isinstance(summary, FailureSummary)


def create_response_envelope(summary: FailureSummary) -> ResponseEnvelope:
    """Create a deterministic response envelope from a trusted summary."""

    if not is_valid_response_summary(summary):
        return ResponseEnvelope(
            status="error",
            summary=FailureSummary(
                category="unknown",
                severity="unknown",
                reason="invalid_response_summary",
                review_required=True,
            ),
        )

    return ResponseEnvelope(
        status="success",
        summary=summary,
    )
