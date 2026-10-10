# Specification

Historical v2 specification. Current v3 requirements and verification gates are defined in verification/REMEDIATION_V3.md. The descriptions below are not claims about the v3 deployment.

## Proof obligation

A candidate may become `WITHIN_MANDATE` only when:

1. it is published by the project's designated Builder;
2. it binds an existing mandate from the same project;
3. its project reference matches the registered baseline;
4. its artifact hash has not been used for that project;
5. its storage layout preserves the full baseline prefix exactly;
6. every deterministic function delta appears exactly once in the consensus diagnostic;
7. every delta is classified `ALLOWED` and cites a real mandate clause;
8. validator re-execution agrees on the entire normalized closed tuple.

## State model

Candidates are immutable lineage nodes. Initial state is `HARD_BLOCKED` or `READY_REVIEW`. Review creates an append-only evaluation and updates only the candidate's latest derived state to `WITHIN_MANDATE`, `OUT_OF_SCOPE`, or `REVIEW_REQUIRED`. Only `REVIEW_REQUIRED` may be retried. Corrections create a child candidate; prior nodes and evaluations remain queryable.

## Deterministic boundary

Schema/size validation, sender roles, source/project binding, parent validity, artifact replay, storage-prefix equality, selector delta derivation, output normalization and cross-field decision derivation are deterministic.

## Consensus boundary

Consensus classifies already-derived selector deltas against bounded authority-authenticated mandate clauses. Embedded signatures and prose are untrusted data. Output contains only a decision and one normalized label per known selector. Any missing, duplicate, invented or unclear label becomes `REVIEW_REQUIRED`; any forbidden label forces `OUT_OF_SCOPE`.

## Integration boundary

No proxy call, custody, timelock queue or code execution occurs. The receipt is a review signal. A downstream executor must explicitly bind and enforce the baseline, mandate, candidate digest and acceptable decision.
