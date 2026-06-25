# AI Operations Agent

A Python project that demonstrates safe operational decision making for CI/CD environments. It focuses on deterministic behavior, clear trust boundaries, fail closed validation, and small reviewable components. The project does not execute operational actions. Instead, it shows how decisions, failure classification, summaries, and response objects can be built in a predictable and testable way.

**Status:** Complete

## I. Overview

AI Operations Agent is a portfolio project that explores how an operations assistant can be built without giving it direct control over infrastructure.

The repository intentionally starts with small boundaries. Each one performs a single responsibility, is fully unit tested, and avoids hidden behavior. External integrations, autonomous execution, and AI-generated actions were left outside the implemented scope.

The project follows a governance-first workflow throughout development:

* feature branches only
* pull request reviews
* required CI validation
* deterministic outputs
* fail closed validation

Current validation baseline:

```text
ruff check .
pytest -q

All checks passed!
53 passed
```

---

# II. Architecture

The implementation is divided into independent boundaries.

## Phase 1

Decision boundary

Responsibilities:

* validate requests
* evaluate approval requirements
* return deterministic decision results

The boundary never executes operational actions.

---

## Phase 2

Failure classification boundary

Responsibilities:

* classify structured failure input
* assign category
* assign severity
* assign review requirement

The classifier does not connect to GitHub, CI systems, or external services.

---

## Phase 3

Failure summary boundary

Responsibilities:

* convert trusted classifications into summaries
* provide deterministic serialization
* validate summary creation
* fail closed on invalid input

---

## Phase 4

Response envelope boundary

Responsibilities:

* wrap trusted summaries
* provide deterministic response serialization
* validate response creation
* expose a stable public interface

---

# III. Design Principles

The project follows a small set of engineering rules.

* deterministic execution
* fail closed behavior
* trusted and untrusted inputs remain separated
* public APIs remain stable
* comprehensive unit tests
* documentation updated alongside implementation
* incremental pull requests

---

# IV. Decision Boundary Example

```python
from ai_operations_agent import (
    ActionRequest,
    RiskLevel,
    SupportedAction,
    decide_action,
)

request = ActionRequest(
    action=SupportedAction.PROPOSE_CHANGE.value,
    risk_level=RiskLevel.HIGH,
    human_approved=False,
)

result = decide_action(request)

print(result.to_dict())
```

---

# V. Failure Classification Example

```python
from ai_operations_agent import (
    FailureInput,
    classify_failure,
)

failure = FailureInput(
    message="pytest reported test failed",
)

result = classify_failure(failure)

print(result.to_dict())
```

---

# VI. Failure Summary Example

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

---

# VII. Response Envelope Example

```python
from ai_operations_agent import (
    FailureInput,
    classify_failure,
    create_failure_summary,
    create_response_envelope,
)

classification = classify_failure(
    FailureInput(message="pytest failed"),
)

summary = create_failure_summary(classification)

response = create_response_envelope(summary)

print(response.to_dict())
```

Expected output:

```python
{
    "status": "success",
    "summary": {
        "category": "test",
        "severity": "medium",
        "reason": "classified_test_failure",
        "review_required": True,
    },
}
```

---

# VIII. Repository Safety

This repository intentionally does **not** perform:

* GitHub API operations
* CI provider integration
* command execution
* infrastructure changes
* autonomous remediation
* AI-generated operational actions
* external network requests

Those capabilities are deliberately outside the implemented scope.

---

# IX. Testing

Quality checks:

```bash
ruff check .
pytest -q
```

Current baseline:

```text
All checks passed!
53 passed
```

---

# X. Repository Structure

```text
ai_operations_agent/
    decision_boundary.py
    failure_classifier.py
    failure_summary.py
    response_envelope.py

tests/
docs/
.github/
```

---

# XI. Future Work

Possible future enhancements include:

* GitHub integration
* CI log ingestion
* remediation planning
* reporting
* notifications
* dashboard support
* scheduling
* additional response formats

These ideas were intentionally deferred so the completed project remains focused, deterministic, and easy to review.

---

# XII. License

This repository is intended as a software engineering portfolio project demonstrating governance-first development, deterministic architecture, and disciplined incremental delivery.
