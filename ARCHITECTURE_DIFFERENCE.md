# Architecture difference statement

Historical v2 description. v3 adds validator retrieval and correspondence review for source artifacts; see verification/REMEDIATION_V3.md.

This project is not a renamed AgentSpend Firewall or a repeated lock/evaluate/settle workflow.

| Dimension | UpgradeMandate Sentinel |
|---|---|
| Product primitive | Append-only proxy-upgrade provenance graph and review receipt |
| Lifecycle | Baseline registration → mandate attachment → candidate lineage node → zero or more immutable evaluations |
| Persistent storage | Separate project, mandate, candidate and evaluation collections plus parent edges and artifact index |
| Evidence flow | Authority publishes baseline/mandate; separately designated Builder publishes candidate; contract derives selector deltas |
| Deterministic gate | Exact baseline storage prefix preservation hard-blocks before consensus |
| Consensus binding | Validators compare the full normalized selector-label tuple, not free-form rationale |
| Downstream effect | Integration receipt for an external timelock/executor; no spending authorization or settlement |
| UI information architecture | Three-pane source/diff cockpit, provenance rail and evaluation trace |

Originality preflight: product primitive, state machine, storage model, evidence roles, consensus tuple, integration effect and interface are all materially different from prior spend, escrow, freshness and claim projects in this workspace.
