from ai_operations_agent.failure_classifier import FailureInput, classify_failure
from ai_operations_agent.failure_summary import FailureSummary, create_failure_summary


def test_failure_summary_stores_structured_fields():
    summary = FailureSummary(
        category="test",
        severity="medium",
        reason="classified_test_failure",
        review_required=True,
    )

    assert summary.category == "test"
    assert summary.severity == "medium"
    assert summary.reason == "classified_test_failure"
    assert summary.review_required is True


def test_failure_summary_serialization_is_stable():
    summary = FailureSummary(
        category="test",
        severity="medium",
        reason="classified_test_failure",
        review_required=True,
    )

    assert summary.to_dict() == {
        "category": "test",
        "severity": "medium",
        "reason": "classified_test_failure",
        "review_required": True,
    }


def test_create_failure_summary_from_classification():
    classification = classify_failure(
        FailureInput(message="pytest failed"),
    )

    summary = create_failure_summary(classification)

    assert summary.to_dict() == {
        "category": "test",
        "severity": "medium",
        "reason": "classified_test_failure",
        "review_required": True,
    }

def test_create_failure_summary_rejects_invalid_classification():
    summary = create_failure_summary(None)  # type: ignore[arg-type]

    assert summary.to_dict() == {
        "category": "unknown",
        "severity": "unknown",
        "reason": "invalid_failure_classification",
        "review_required": True,
    }
