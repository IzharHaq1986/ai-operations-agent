# project_state.md

## Project

AI Operations Agent

## Current Phase

Phase 0 — Architecture Definition & Governance Baseline

Status: In Progress

---

## Project Vision

Build an AI-powered operations platform capable of observing DevOps signals, analyzing failures, producing actionable recommendations, and enforcing safe operational guardrails before executing high-risk actions.

The system must prioritize:

* Deterministic behavior
* Auditability
* Human approval workflows
* Safe operational boundaries
* Clear separation between observation, reasoning, and action

---

## Problem Statement

Traditional CI/CD automation executes predefined workflows but does not understand operational outcomes.

Engineering teams still spend significant time:

* Reading CI/CD logs
* Diagnosing failures
* Determining root causes
* Drafting remediation steps
* Creating issues and release documentation
* Reviewing operational risk

The AI Operations Agent aims to reduce this manual effort through structured analysis and decision support.

---

## High-Level Goal

Transform DevOps telemetry into actionable operational intelligence.

From:

"Automation executes workflows."

To:

"Agent understands workflow outcomes and recommends safe next actions."

---

## Scope (Minimum Viable Product)

### Included

* CI/CD log ingestion
* Failure analysis
* Failure summarization
* Root-cause categorization
* Suggested remediation generation
* Risk classification
* Safe next-action recommendations
* Audit logging
* Human approval gates

### Excluded

* Autonomous production deployments
* Autonomous infrastructure modifications
* Autonomous pull request merges
* Autonomous credential management
* Autonomous approval bypasses

---

## Architectural Principles

### Principle 1

Observation must be separated from action.

### Principle 2

All high-risk actions require explicit human approval.

### Principle 3

Agent recommendations must be explainable.

### Principle 4

Operational events must be auditable.

### Principle 5

Failure analysis should be reproducible.

### Principle 6

No hidden decision pathways.

---

## Proposed Technology Stack

### Backend

* Python 3.12+
* FastAPI

### AI Layer

* OpenAI API (future integration)
* Structured prompt framework
* Deterministic response validation

### DevOps

* GitHub Actions
* Docker
* Docker Compose

### Storage

* SQLite (initial)
* PostgreSQL (future)

### Testing

* Pytest
* Ruff
* Coverage

---

## Development Roadmap

### Phase 1

CI/CD Foundation

Status: Complete (existing DevOps CI/CD Showcase)

Objectives:

* GitHub Actions
* Docker deployment
* Health checks
* Rollback awareness

---

### Phase 2

Failure Analysis Service

Status: Not Started

Deliverables:

POST /analyze-ci-failure

Input:

* CI/CD logs

Output:

* Failure summary
* Likely root cause
* Suggested fix
* Risk classification
* Recommended next action

---

### Phase 3

GitHub Workflow Integration

Status: Not Started

Deliverables:

* Read workflow runs
* Detect failures
* Collect logs
* Generate issue drafts

---

### Phase 4

Operational Risk Engine

Status: Not Started

Deliverables:

* Severity classification
* Confidence scoring
* Action recommendations

---

### Phase 5

Approval & Guardrails

Status: Not Started

Deliverables:

* Human approval workflow
* Action authorization layer
* Protected operation policies

---

### Phase 6

Audit & Compliance

Status: Not Started

Deliverables:

* Decision history
* Action history
* Approval history
* Operational reporting

---

## Trust Boundaries

### Trusted

* FastAPI application
* Validation layer
* Policy engine
* Approval engine

### Untrusted

* AI model outputs
* External logs
* User inputs
* Third-party integrations

All untrusted data must pass validation before influencing operational decisions.

---

## Success Criteria

The project successfully demonstrates:

1. AI-assisted CI/CD failure analysis.
2. Structured operational recommendations.
3. Human-in-the-loop governance.
4. Safe operational boundaries.
5. Auditability of recommendations and actions.
6. Production-quality engineering practices.

---

## Repository Governance

### Branch Protection

Required

### Pull Requests

Required

### CI Checks

Required

### Direct Commits to Main

Prohibited

### Squash Merge

Required

---

## Current Status Summary

Project initialized.

Architecture definition underway.

No production code implemented.

No AI integrations implemented.

No GitHub integrations implemented.

Next Milestone:

Phase 0 completion and architecture review.
