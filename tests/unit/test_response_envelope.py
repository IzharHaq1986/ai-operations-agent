from ai_operations_agent.failure_summary import FailureSummary

from ai_operations_agent.response_envelope import (
    ResponseEnvelope,
    create_response_envelope,
)


def test_response_envelope_stores_summary():
    summary = FailureSummary(
        category="test",
        severity="medium",
        reason="classified_test_failure",
        review_required=True,
    )

    envelope = ResponseEnvelope(
        status="success",
        summary=summary,
    )

    assert envelope.status == "success"
    assert envelope.summary is summary

def test_response_envelope_serialization_is_stable():
    summary = FailureSummary(
        category="test",
        severity="medium",
        reason="classified_test_failure",
        review_required=True,
    )

    envelope = ResponseEnvelope(
        status="success",
        summary=summary,
    )

    assert envelope.to_dict() == {
        "status": "success",
        "summary": {
            "category": "test",
            "severity": "medium",
            "reason": "classified_test_failure",
            "review_required": True,
        },
    }

def test_create_response_envelope_from_valid_summary():
    summary = FailureSummary(
        category="test",
        severity="medium",
        reason="classified_test_failure",
        review_required=True,
    )

    envelope = create_response_envelope(summary)

    assert envelope.to_dict() == {
        "status": "success",
        "summary": {
            "category": "test",
            "severity": "medium",
            "reason": "classified_test_failure",
            "review_required": True,
        },
    }


def test_create_response_envelope_rejects_invalid_summary():
    envelope = create_response_envelope(None)  # type: ignore[arg-type]

    assert envelope.to_dict() == {
        "status": "error",
        "summary": {
            "category": "unknown",
            "severity": "unknown",
            "reason": "invalid_response_summary",
            "review_required": True,
        },
    }
