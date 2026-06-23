from ai_operations_agent.failure_classifier import (
    FailureCategory,
    FailureClassification,
    FailureInput,
    FailureReason,
    FailureSeverity,
    FailureStatus,
    classify_failure,
    is_valid_failure_input,
)


def test_missing_failure_input_is_rejected():
    result = classify_failure(None)

    assert result.status == FailureStatus.REJECTED
    assert result.reason == FailureReason.INVALID_FAILURE_INPUT.value
    assert result.category == FailureCategory.UNKNOWN
    assert result.severity == FailureSeverity.UNKNOWN
    assert result.review_required is True


def test_blank_failure_message_is_rejected():
    result = classify_failure(FailureInput(message=" "))

    assert result.status == FailureStatus.REJECTED
    assert result.reason == FailureReason.INVALID_FAILURE_INPUT.value


def test_dependency_failure_is_classified():
    result = classify_failure(FailureInput(message="ImportError: missing package"))

    assert result.category == FailureCategory.DEPENDENCY
    assert result.severity == FailureSeverity.MEDIUM
    assert result.review_required is True


def test_test_failure_is_classified():
    result = classify_failure(FailureInput(message="pytest reported test failed"))

    assert result.category == FailureCategory.TEST
    assert result.severity == FailureSeverity.MEDIUM
    assert result.review_required is True


def test_lint_failure_is_classified():
    result = classify_failure(FailureInput(message="ruff lint failure"))

    assert result.category == FailureCategory.LINT
    assert result.severity == FailureSeverity.LOW
    assert result.review_required is False


def test_configuration_failure_is_classified():
    result = classify_failure(FailureInput(message="yaml configuration error"))

    assert result.category == FailureCategory.CONFIGURATION
    assert result.severity == FailureSeverity.HIGH
    assert result.review_required is True


def test_unknown_failure_is_classified_as_unknown():
    result = classify_failure(FailureInput(message="unexpected runner issue"))

    assert result.category == FailureCategory.UNKNOWN
    assert result.severity == FailureSeverity.UNKNOWN
    assert result.review_required is True


def test_failure_classification_serialization_is_stable():
    result = classify_failure(FailureInput(message="ruff lint failure"))

    assert result.to_dict() == {
        "status": "classified",
        "reason": "classified_lint_failure",
        "category": "lint",
        "severity": "low",
        "review_required": False,
    }


def test_valid_failure_input_returns_true():
    assert is_valid_failure_input(FailureInput(message="pytest failed")) is True


def test_invalid_failure_input_returns_false():
    assert is_valid_failure_input(None) is False


def test_failure_classification_type_is_available():
    assert FailureClassification is not None


def test_non_string_failure_message_is_rejected():
    result = classify_failure(
        FailureInput(message=404),  # type: ignore[arg-type]
    )

    assert result.status == FailureStatus.REJECTED
    assert result.reason == FailureReason.INVALID_FAILURE_INPUT.value
    assert result.category == FailureCategory.UNKNOWN
    assert result.severity == FailureSeverity.UNKNOWN
    assert result.review_required is True


def test_failure_classification_is_case_insensitive():
    result = classify_failure(
        FailureInput(message="PyTest Reported TEST FAILED"),
    )

    assert result.status == FailureStatus.CLASSIFIED
    assert result.reason == FailureReason.CLASSIFIED_TEST_FAILURE.value
    assert result.category == FailureCategory.TEST
    assert result.severity == FailureSeverity.MEDIUM
    assert result.review_required is True

def test_dependency_failure_classification_is_case_insensitive():
    result = classify_failure(
        FailureInput(message="IMPORTERROR: Missing Package"),
    )

    assert result.status == FailureStatus.CLASSIFIED
    assert result.reason == FailureReason.CLASSIFIED_DEPENDENCY_FAILURE.value
    assert result.category == FailureCategory.DEPENDENCY
    assert result.severity == FailureSeverity.MEDIUM
    assert result.review_required is True

def test_lint_failure_classification_is_case_insensitive():
    result = classify_failure(
        FailureInput(message="RUFF LINT FAILURE"),
    )

    assert result.status == FailureStatus.CLASSIFIED
    assert result.reason == FailureReason.CLASSIFIED_LINT_FAILURE.value
    assert result.category == FailureCategory.LINT
    assert result.severity == FailureSeverity.LOW
    assert result.review_required is False

def test_configuration_failure_classification_is_case_insensitive():
    result = classify_failure(
        FailureInput(message="YAML CONFIGURATION ERROR"),
    )

    assert result.status == FailureStatus.CLASSIFIED
    assert result.reason == FailureReason.CLASSIFIED_CONFIGURATION_FAILURE.value
    assert result.category == FailureCategory.CONFIGURATION
    assert result.severity == FailureSeverity.HIGH
    assert result.review_required is True
