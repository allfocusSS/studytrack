# Development Process

## Source of tasks

Before a GitHub repository exists, `_docs/tasks.md` and `_docs/issues/` hold the initial task list and draft issue bodies. No implementation should begin during this preparation stage.

After the tasks are transferred, the live GitHub issues are the only active backlog. Update drafts only as historical references; groom and discuss actual work in GitHub.

Read acceptance criteria before starting and before closing an issue. Commit regularly.

## Roles

- PM grooms a task using [_docs/team/pm.md](team/pm.md).
- Engineer implements a groomed task using [_docs/team/software-engineer.md](team/software-engineer.md).
- QA independently verifies it using [_docs/team/qa-engineer.md](team/qa-engineer.md).

## Orchestrator

The main session is the orchestrator. It launches PM, engineer, and QA as separate subagents. It handles issue ordering, handoffs, integration, and closure; it does not groom, implement, or test its own work.

Use one issue at a time for this small MVP. The initial dependency order is bootstrap, accounts, assignment CRUD, status/overdue behaviour, filters/sorting, then final integration and documentation. Record real issue numbers after creation rather than assuming they match local task IDs.

## Lifecycle

1. Pick the next open issue whose prerequisites are complete.
2. Launch a PM subagent to read the issue and linked documents, refine it to the four-section template, and post a grooming summary.
3. Launch an engineer subagent to implement exactly those acceptance criteria, run tests, commit, and leave an implementation comment. The issue remains open.
4. Launch an independent QA subagent. It checks each criterion against the actual code, runs the necessary tests, and posts `QA: PASS` or `QA: FAIL` with evidence.
5. On FAIL, return to the engineer with QA's findings. Repeat the QA step after corrections.
6. On PASS, the orchestrator integrates and pushes the reviewed commit, checks that the live issue still matches the verified criteria, then closes it as completed.
7. Repeat until every MVP issue has been implemented, verified, pushed, and closed.

The stop condition is checkable: every MVP issue is closed following QA PASS and the latest committed full test suite passes. Merely adding a closing comment does not satisfy this condition.

If the tool supports `/goal`, it can drive this lifecycle. Otherwise continue the same loop explicitly; do not assume a slash command is available.

## Evidence

An implementation comment states what changed, the commit, the tests actually run, their actual results, and any unresolved limitation.

A QA comment lists every acceptance criterion, its PASS/FAIL verdict, the exact check or test used, the tested commit, and the actual command results. A single failed criterion means FAIL.

Templates are examples, not evidence. Fill them with observed facts; never post placeholder test counts as if tests ran.

## Deadline

Record the course's exact deadline and timezone in `_docs/decisions.md`. GitHub `created_at` and `closed_at` must both be before that deadline for counted issues. Do not backdate or recreate evidence. If a required issue remains unfinished, report that fact.

## Local and remote work

Preserve unrelated changes. Use the connected repository for source history. Include the issue number in meaningful implementation commit messages. A local commit alone is not a submission; push the reviewed source before closure.

Do not fabricate a repository URL when none exists. If access or an external action is unavailable, finish the preparation that can be completed and request the missing repository/access information.
