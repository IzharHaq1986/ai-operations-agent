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
