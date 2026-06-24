from ai_operations_agent.failure_summary import FailureSummary


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
