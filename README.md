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
