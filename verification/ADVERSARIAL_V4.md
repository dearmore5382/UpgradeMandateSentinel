# Live conflict and authorization matrix

Status: PASS, completed 2026-10-10T02:25:25.733Z. Exact contract: `0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B`, StudioNet, version 4. All 13 transactions FINALIZED and all 13 post-state assertions passed.

Script: run-v4-adversarial.mjs. Evidence: LIVE_V4_ADVERSARIAL.json (hashes saved before polling, actual transaction/consensus responses and post-state captured).
The script refuses to overwrite an existing evidence file. Never blindly rerun a partially completed on-chain lifecycle.

## Predeclared expectations

| Attack | Required observation |
| --- | --- |
| Builder publishes authority mandate | AUTHORITY_ONLY; no counter/record mutation |
| Authority submits as Builder | BUILDER_ONLY; no mutation |
| Same artifact submitted twice | ARTIFACT_ALREADY_USED; no mutation |
| Reevaluate positive terminal result | NOT_REVIEWABLE; no extra evaluation |
| Reevaluate integrity failure | NOT_REVIEWABLE; no extra evaluation |
| Bind another project's mandate | INVALID_BINDING; no mutation |
| Bind another project's parent | INVALID_PARENT; no mutation |
| Substitute repository | REPOSITORY_MISMATCH; no mutation |
| Explicit allow and forbidden FEE_ROUNDING | Both fetched artifacts MATCH, result OUT_OF_SCOPE, selector 0x1b55c7e5 FORBIDDEN |
| Evaluate conflict using Authority, not Builder | Allowed permissionless review; caller recorded |
| Conflict against fresh project | Previously finalized project/mandate/candidate/evaluation remain unchanged |
| Reevaluate conflict terminal result | NOT_REVIEWABLE; no extra evaluation |

Actors are the two existing auxiliary wallets, not the deployer. All transaction values are zero. This contract creates review receipts, not monetary transfers or executed upgrades.
Public fixture bytes are unchanged and pinned to commit 4f91e189810e6e5f266152661de25fba00cb26a2. They are authored synthetic artifact fixtures. Conflict is an authenticated policy fixture, not a claim about a real external governance decision.

This is a bounded self-audit, not proof against every possible attack, not forced validator disagreement, and not a browser-wallet signing test.

## Captured results

Every matrix row above passed. `node verification/check-v4-adversarial.mjs` separately validates 10 expected leader return values, successful execution, FINALIZED status, and at least 3 captured agreeing votes per checked transaction. A trailing idle/cancelled leader rotation is retained, not misclassified as the successful execution.

Conflict project 2, mandate 2, candidate 5: actual fetched baseline and candidate both MATCH. The explicit forbidden FEE_ROUNDING capability overrode the allowing clause; outcome OUT_OF_SCOPE, selector 0x1b55c7e5 FORBIDDEN. Authority called evaluation successfully, proving it is not Builder-only. Prior project 1, mandate 1, candidate 1 and evaluation 1 remained unchanged. Final counters: projects 3, mandates 3, candidates 6, evaluations 3.

- Authority-only attack: `0xa014bc3af8609abc1a273557c98ba12521a626aefc5a6dfba7350176d3ca0ac2`.
- Builder-only attack: `0x3adbf451c225afbd731a40455445ecfd14d09321656216d8265bed65a7759a23`.
- Conflict evaluation: `0xec1e4426991198cee9b3cc3e9c497087588264b3a9bd65f3c43abb6a5fd06f05`.
- Terminal conflict replay: `0xb715fdc24f0002977bfe36d28a0aa2ff9a9cbb5b1ffcf22f0b19243531d888b5`.

Full hashes, inputs, signers, leader execution, votes and snapshots are in LIVE_V4_ADVERSARIAL.json. Rejections are successful contract executions returning a denial code, not necessarily failed blockchain transactions. The invariant is denial plus no unauthorized state mutation.
