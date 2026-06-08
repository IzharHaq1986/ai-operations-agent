# Repository Governance Workflow

## Purpose

This document defines the repository workflow used by the AI Operations Agent project.

The objective is to maintain a consistent development process, reduce operational risk, and ensure all changes are reviewed before entering the protected main branch.

This workflow applies to documentation, configuration, tests, infrastructure, and application code.

---

## Governance Principles

### Review Before Merge

All changes must be reviewed before becoming part of the main branch.

Direct modification of the protected main branch is not permitted.

### Small and Reviewable Changes

Changes should remain focused and easy to review.

Large unrelated changes should be divided into multiple pull requests.

### Documentation Before Implementation

Architecture, governance, and safety decisions should be documented before implementation begins.

### Safety Before Automation

Automation should not bypass review, approval, authorization, or audit requirements.

---

## Branch Strategy

### Main Branch

The main branch serves as the project's source of truth.

Responsibilities:

* Stable project baseline
* Approved documentation
* Approved implementation work
* Approved architecture decisions

Requirements:

* Protected branch
* Pull requests required
* Direct commits prohibited

### Working Branches

All work must be performed on dedicated branches.

Examples:

```text
docs/update-governance-documentation
docs/architecture-review

feat/failure-analysis-service
feat/github-integration

test/add-analysis-tests

chore/repository-maintenance
```

Branch names should clearly communicate intent.

---

## Pull Request Workflow

### Step 1

Create a branch from the latest main branch.

### Step 2

Implement only the intended change.

Avoid unrelated modifications.

### Step 3

Review changes locally.

Confirm:

* intended files only
* no temporary files
* no unintended formatting changes

### Step 4

Push the branch.

### Step 5

Create a pull request.

Use the approved PR template structure.

### Step 6

Address review feedback if required.

### Step 7

Merge after approval.

---

## Pull Request Description Standard

Every pull request should contain:

### I. Summary

Brief description of the change.

### II. What Changed

List of modifications.

### III. Why This Matters

Reason for the change.

### IV. Impact

Expected impact on the project.

### V. Verification

Validation steps performed.

### Pre-Flight Check

Project safety checklist.

The Pre-Flight Check section must remain part of the Markdown document and must not be placed inside a fenced code block.

---

## Merge Policy

### Preferred Merge Method

Squash merge.

Benefits:

* Cleaner history
* Easier review
* Easier auditing

### Before Merge

Confirm:

* review completed
* branch protection satisfied
* intended scope maintained
* no temporary files committed

---

## Post-Merge Cleanup

After a successful merge:

### Local Cleanup

Delete merged branch locally.

Example:

```bash
git branch -d branch-name
```

### Remote Cleanup

Delete merged branch remotely.

Example:

```bash
git push origin --delete branch-name
```

### Synchronize Main

Update local main branch.

Example:

```bash
git checkout main
git pull origin main
```

Working tree should be clean before beginning new work.

---

## Temporary File Handling

Temporary files should not be committed.

Examples:

```text
pr.md
scratch.md
notes.tmp
```

If temporary files are used during PR creation, remove them before merge.

---

## Documentation Expectations

Documentation should:

* explain decisions
* explain rationale
* reduce ambiguity
* remain maintainable

Documentation should avoid unnecessary complexity.

---

## Main Branch Protection Requirements

The main branch should remain protected.

Minimum protections:

* pull requests required
* force pushes blocked
* branch deletion restricted
* approval required before merge
* conversations resolved before merge

Additional protections may be added as the project evolves.

---

## Future CI Requirements

When CI workflows are introduced:

* status checks should be required before merge
* failed checks should block merge
* protected branch rules should enforce compliance

Until CI exists, governance controls remain review-based.

---

## Repository Safety Expectations

All future development should follow the trust model defined in project_state.md.

Key expectations:

* AI agents treated as untrusted
* human approval required for high-risk actions
* least-privilege access
* validated inputs
* auditable decisions
* separation of trusted and untrusted contexts

---

## Success Criteria

This workflow is successful when:

* main remains stable
* changes are reviewable
* repository history remains clean
* governance remains consistent
* operational risk is reduced

---

## Pre-Flight Check

* Main branch remains protected.
* Pull request workflow remains enforced.
* No direct commits to main.
* Documentation remains consistent with project_state.md.
* Temporary PR files removed before merge.
* No governance bypass introduced.
* No security controls weakened.
* Repository history remains reviewable.
