# AI Operations Agent

AI-powered operational intelligence platform for CI/CD analysis,
failure classification, remediation recommendations, and safe
human-approved operational actions.

Status: Architecture Definition

## Decision Boundary Example

The first Phase 1 implementation slice adds a deterministic approval and risk decision boundary.

It does not execute tools, call models, or perform operational actions. It only evaluates a request and returns a safe decision.

```python
from ai_operations_agent import ActionRequest, RiskLevel, SupportedAction, decide_action

request = ActionRequest(
    action=SupportedAction.PROPOSE_CHANGE.value,
    risk_level=RiskLevel.HIGH,
    human_approved=False,
)

result = decide_action(request)

print(result.to_dict())
```

## Failure Classification Example

Phase 2 adds a deterministic failure-classification boundary.

It does not ingest live CI logs, call GitHub, call models, execute tools, or perform remediation. It only classifies explicitly provided structured failure text.

```python
from ai_operations_agent import FailureInput, classify_failure

failure = FailureInput(
    message="pytest reported test failed",
)

result = classify_failure(failure)

print(result.to_dict())
```

## Failure Summary Example

The failure summary boundary converts a trusted failure classification into a deterministic, structured summary suitable for operator-facing output.

```python
from ai_operations_agent import (
    FailureInput,
    classify_failure,
    create_failure_summary,
)

classification = classify_failure(
    FailureInput(message="pytest failed"),
)

summary = create_failure_summary(classification)

print(summary.to_dict())
```

Expected output:

```python
{
    "category": "test",
    "severity": "medium",
    "reason": "classified_test_failure",
    "review_required": True,
}
```

The failure summary boundary:

* accepts trusted `FailureClassification` objects
* returns deterministic structured output
* preserves fail-closed behavior
* performs no external I/O
* performs no model calls
* performs no tool execution
* performs no autonomous actions
