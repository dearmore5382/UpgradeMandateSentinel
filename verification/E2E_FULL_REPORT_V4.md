# UpgradeMandate Sentinel — Consolidated v4 E2E Evidence

Verified date: 2026-10-10. This is the single submission report; raw JSON remains linked for independent inspection.

## 1. Release identity and verification summary

- Network: GenLayer StudioNet; contract version 4, schema artifact-bound-upgrade-review-v4.
- [Contract](https://explorer-studio.genlayer.com/address/0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B): `0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B`.
- [Production application](https://upgrade-mandate-sentinel.dearmorescheuer5382.workers.dev).
- Deployed source exact-byte parity SHA-256: `f471a6a4f26ef3c25667a5996b8ea50b1ef8a896e61c3dc37951976e5c961689`; RPC gen_getContractCode decoded from base64.
- Positive/integrity lifecycle: 10 FINALIZED transactions, 13 recorded assertions passed (including public-source preflights).
- Conflict/authorization: 13 FINALIZED transactions, 13 recorded assertions passed; 10 expected leader return values independently validated with at least 3 agreeing votes each.
- Total successful verification suites: 23 FINALIZED transactions. The earlier ambiguous-mandate attempt is separately retained below and not counted as a passing happy path.
- Local production-contract regressions: 19 passed; frontend build passed. Model/network mocks in local tests are not live-consensus proof.
- Production rendered readback parity confirmed for candidates 1 and 2. Browser-signed lifecycle/account switching remains unverified.

## 2. What changed and why it addresses artifact correspondence

Publisher authentication alone was insufficient. Validators now retrieve full-commit-pinned manifests and their referenced Solidity source, compute both SHA-256 digests, and consume the entire supported source grammar. Actual function signatures/selectors and ordered storage must match the manifest inventory before semantic review. Hidden mint functions fail inventory checks; unsupported source fails closed. Capability meaning and mandate review receive fetched source bodies, not claimant-written summaries as a substitute. Unknown authorization produces REVIEW_REQUIRED. Explicit forbidden capabilities override allowing clauses deterministically.

This is deliberately restricted standalone source review: one contract, uint256 internal storage and supported external functions. It is not a general Solidity compiler, whole-repository attestation, compiled/deployed-bytecode attestation or proxy upgrade executor. Unsupported constructs are rejected.

## 3. Actors, resources and provenance

- Authority: `0x686269f09C21aac57f39662855FA51b9758698b2`.
- Designated Builder: `0x48CCA889CF67A8420D82341e2fa9532Dc36Ba5c2`.
- Deployer signed no workflow transaction in these suites; no deployer allowlist is required for a reviewer to register a fresh project.
- Immutable [fixture directory](https://github.com/dearmore5382/UpgradeMandateSentinel/tree/4f91e189810e6e5f266152661de25fba00cb26a2/samples/artifacts) at commit `4f91e189810e6e5f266152661de25fba00cb26a2`.
- Fixtures are authored synthetic test artifacts and policy declarations, not independent evidence of real-world governance adoption. They prove handling of these exact source bytes and authenticated test policies. Public manifest/source HTTP bytes and SHA-256 were separately checked before the positive suite.
- All adversarial transactions attach zero value. No monetary payout, custody or executed upgrade is claimed.

## 4. Happy path and integrity failures — all 10 transactions

[Raw evidence with inputs/signers/readbacks](LIVE_RUN_V4_EXACT_MANDATE.json). All rows below reached FINALIZED. Counters are P/M/C/E = projects/mandates/candidates/evaluations. A denial code is a successful contract execution refusing the action, not necessarily a failed blockchain transaction.

| # | Action | Signer | Before → after P/M/C/E | Leader return / consensus | Explorer transaction |
| --- | --- | --- | --- | --- | --- |
| 1 | baseline | Authority | 1/1/1/1 → 2/1/1/1 | Not captured in this suite; outcome independently read back | [0x13f298c109aa721a7d498cf981f877496363dec78963ba8fdb15b880d5b10157](https://explorer-studio.genlayer.com/tx/0x13f298c109aa721a7d498cf981f877496363dec78963ba8fdb15b880d5b10157) |
| 2 | mandate | Authority | 2/1/1/1 → 2/2/1/1 | Not captured in this suite; outcome independently read back | [0x40e933396e78040be690e73a5166e3761cc2cffb1f80a4297e57b82a77945b5b](https://explorer-studio.genlayer.com/tx/0x40e933396e78040be690e73a5166e3761cc2cffb1f80a4297e57b82a77945b5b) |
| 3 | submit safe | Builder | 2/2/1/1 → 2/2/2/1 | Not captured in this suite; outcome independently read back | [0xeac02b44f4149a7893ca8c6f9e6796924d1798f2fd859ddeb23f64bca15f5296](https://explorer-studio.genlayer.com/tx/0xeac02b44f4149a7893ca8c6f9e6796924d1798f2fd859ddeb23f64bca15f5296) |
| 4 | evaluate safe | Builder | 2/2/2/1 → 2/2/2/2 | Not captured in this suite; outcome independently read back | [0xc22edaeb147cb9fec5935d87ddcfdb4e5bbca4edd99e79c23383322e6de46f5f](https://explorer-studio.genlayer.com/tx/0xc22edaeb147cb9fec5935d87ddcfdb4e5bbca4edd99e79c23383322e6de46f5f) |
| 5 | submit hidden-mint | Builder | 2/2/2/2 → 2/2/3/2 | Not captured in this suite; outcome independently read back | [0xbe013c6a74c6a3a5d0c58b024a2bdf75e176b8f675175335d8fa03136f46418c](https://explorer-studio.genlayer.com/tx/0xbe013c6a74c6a3a5d0c58b024a2bdf75e176b8f675175335d8fa03136f46418c) |
| 6 | evaluate hidden-mint | Builder | 2/2/3/2 → 2/2/3/2 | Not captured in this suite; outcome independently read back | [0x2e6f9f7f735d10040ce56e78910d073705bf10ff52dd2b72516b4f5ff509725a](https://explorer-studio.genlayer.com/tx/0x2e6f9f7f735d10040ce56e78910d073705bf10ff52dd2b72516b4f5ff509725a) |
| 7 | submit wrong-storage | Builder | 2/2/3/2 → 2/2/4/2 | Not captured in this suite; outcome independently read back | [0x706fa5f07414749478535cf0bc0960406da127f8b2aec28018828b08dbf3f1d1](https://explorer-studio.genlayer.com/tx/0x706fa5f07414749478535cf0bc0960406da127f8b2aec28018828b08dbf3f1d1) |
| 8 | evaluate wrong-storage | Builder | 2/2/4/2 → 2/2/4/2 | Not captured in this suite; outcome independently read back | [0x4c069276c6e3e908acbf0bd34ad2d0ffe9e97b789157ec9ac7d41c58343cb5dc](https://explorer-studio.genlayer.com/tx/0x4c069276c6e3e908acbf0bd34ad2d0ffe9e97b789157ec9ac7d41c58343cb5dc) |
| 9 | submit bad digest | Builder | 2/2/4/2 → 2/2/5/2 | Not captured in this suite; outcome independently read back | [0x197e3bc3aed5c1878757507098f21ab95911105a6dd058a71bd7ead0fca9de80](https://explorer-studio.genlayer.com/tx/0x197e3bc3aed5c1878757507098f21ab95911105a6dd058a71bd7ead0fca9de80) |
| 10 | evaluate bad digest | Builder | 2/2/5/2 → 2/2/5/2 | Not captured in this suite; outcome independently read back | [0x7a235cb906136223b8e898706ae666c5b2ca4b55f3eca8a2bda71f2e74d701bc](https://explorer-studio.genlayer.com/tx/0x7a235cb906136223b8e898706ae666c5b2ca4b55f3eca8a2bda71f2e74d701bc) |

### Observed case outcomes

| Candidate | Expected and observed | Verification consequence |
| --- | --- | --- |
| 1 | WITHIN_MANDATE; baseline MATCH, candidate MATCH | Exact clause M-01 authorizes preserved deposit and added roundFee |
| 2 | INTEGRITY_FAILURE; MISMATCH | Hidden mint omitted from manifest; no evaluation record |
| 3 | INTEGRITY_FAILURE; UNSUPPORTED_SOURCE | Address storage outside supported grammar; no evaluation record |
| 4 | INTEGRITY_FAILURE; MANIFEST_DIGEST_MISMATCH | Zero claimed digest rejected; evaluation counter unchanged |

Final suite counters: 2/2/5/2.

## 5. Conflict and adversarial authorization — all 13 transactions

[Raw evidence with inputs/signers/readbacks](LIVE_V4_ADVERSARIAL.json). All rows below reached FINALIZED. Counters are P/M/C/E = projects/mandates/candidates/evaluations. A denial code is a successful contract execution refusing the action, not necessarily a failed blockchain transaction.

| # | Action | Signer | Before → after P/M/C/E | Leader return / consensus | Explorer transaction |
| --- | --- | --- | --- | --- | --- |
| 1 | builder cannot publish authority mandate | Builder | 2/2/5/2 → 2/2/5/2 | "AUTHORITY_ONLY" / agree=3 | [0xa014bc3af8609abc1a273557c98ba12521a626aefc5a6dfba7350176d3ca0ac2](https://explorer-studio.genlayer.com/tx/0xa014bc3af8609abc1a273557c98ba12521a626aefc5a6dfba7350176d3ca0ac2) |
| 2 | authority cannot impersonate designated builder | Authority | 2/2/5/2 → 2/2/5/2 | "BUILDER_ONLY" / agree=3 | [0x3adbf451c225afbd731a40455445ecfd14d09321656216d8265bed65a7759a23](https://explorer-studio.genlayer.com/tx/0x3adbf451c225afbd731a40455445ecfd14d09321656216d8265bed65a7759a23) |
| 3 | duplicate artifact cannot be submitted again | Builder | 2/2/5/2 → 2/2/5/2 | "ARTIFACT_ALREADY_USED" / agree=3 | [0x7bd35199a145be77b9bb8eb9a2cee3821a057ac0ff7a24695b84cb05e41f8b35](https://explorer-studio.genlayer.com/tx/0x7bd35199a145be77b9bb8eb9a2cee3821a057ac0ff7a24695b84cb05e41f8b35) |
| 4 | finalized positive cannot be evaluated again | Authority | 2/2/5/2 → 2/2/5/2 | "NOT_REVIEWABLE" / agree=4 | [0x1bc16dd4826001ae2a0c944717b2ca98765b56a47d791c5396068cc69116cd3c](https://explorer-studio.genlayer.com/tx/0x1bc16dd4826001ae2a0c944717b2ca98765b56a47d791c5396068cc69116cd3c) |
| 5 | integrity failure cannot be evaluated again | Builder | 2/2/5/2 → 2/2/5/2 | "NOT_REVIEWABLE" / agree=3 | [0x016b4be93dffa4719d918d9739f394aa86124a342aa348992ac954199090ab53](https://explorer-studio.genlayer.com/tx/0x016b4be93dffa4719d918d9739f394aa86124a342aa348992ac954199090ab53) |
| 6 | create isolated conflict project | Authority | 2/2/5/2 → 3/2/5/2 | 2 / agree=3 | [0x162f2739d8ddd037c00c881e523fc6679c80d770f942f500e499f7dde81ab24d](https://explorer-studio.genlayer.com/tx/0x162f2739d8ddd037c00c881e523fc6679c80d770f942f500e499f7dde81ab24d) |
| 7 | publish allow-versus-forbid conflict | Authority | 3/2/5/2 → 3/3/5/2 | 2 / agree=3 | [0x79fbaf29b946dd694ef5cd5d3eeee12de8ce65053c93c67feb71c8e596bb4aa6](https://explorer-studio.genlayer.com/tx/0x79fbaf29b946dd694ef5cd5d3eeee12de8ce65053c93c67feb71c8e596bb4aa6) |
| 8 | cross-project mandate binding rejected | Builder | 3/3/5/2 → 3/3/5/2 | "INVALID_BINDING" / agree=5 | [0xd34055c594c0112a6a89fd917cc39843160f793380c6e815ffe5cbdbf31a7a01](https://explorer-studio.genlayer.com/tx/0xd34055c594c0112a6a89fd917cc39843160f793380c6e815ffe5cbdbf31a7a01) |
| 9 | cross-project parent binding rejected | Builder | 3/3/5/2 → 3/3/5/2 | "INVALID_PARENT" / agree=3 | [0x255658011be9a432825b65b4dc6a7244770926d9b8a4a3f105d24859d67a03a7](https://explorer-studio.genlayer.com/tx/0x255658011be9a432825b65b4dc6a7244770926d9b8a4a3f105d24859d67a03a7) |
| 10 | repository substitution rejected | Builder | 3/3/5/2 → 3/3/5/2 | "REPOSITORY_MISMATCH" / agree=5 | [0xe240347761b940b628db4dad0032e304a62b730b6cd29d96ccd8f22e769e2e33](https://explorer-studio.genlayer.com/tx/0xe240347761b940b628db4dad0032e304a62b730b6cd29d96ccd8f22e769e2e33) |
| 11 | builder submits conflicting candidate | Builder | 3/3/5/2 → 3/3/6/2 | 5 / agree=3 | [0x5d179564a3839c597bf45402caef26b13e1fdd7997769b67e06bc555589fa3c1](https://explorer-studio.genlayer.com/tx/0x5d179564a3839c597bf45402caef26b13e1fdd7997769b67e06bc555589fa3c1) |
| 12 | non-builder reviewer evaluates conflict | Authority | 3/3/6/2 → 3/3/6/3 | "OUT_OF_SCOPE" / agree=3 | [0xec1e4426991198cee9b3cc3e9c497087588264b3a9bd65f3c43abb6a5fd06f05](https://explorer-studio.genlayer.com/tx/0xec1e4426991198cee9b3cc3e9c497087588264b3a9bd65f3c43abb6a5fd06f05) |
| 13 | conflict terminal result cannot be reevaluated | Builder | 3/3/6/3 → 3/3/6/3 | "NOT_REVIEWABLE" / agree=3 | [0xb715fdc24f0002977bfe36d28a0aa2ff9a9cbb5b1ffcf22f0b19243531d888b5](https://explorer-studio.genlayer.com/tx/0xb715fdc24f0002977bfe36d28a0aa2ff9a9cbb5b1ffcf22f0b19243531d888b5) |

### Assertions and protected state

- exact v4 identity: **PASS**.
- builder cannot publish authority mandate: **PASS**.
- authority cannot impersonate designated builder: **PASS**.
- duplicate artifact cannot be submitted again: **PASS**.
- finalized positive cannot be evaluated again: **PASS**.
- integrity failure cannot be evaluated again: **PASS**.
- cross-project mandate binding rejected: **PASS**.
- cross-project parent binding rejected: **PASS**.
- repository substitution rejected: **PASS**.
- explicit forbidden capability wins over allowing clause: **PASS**.
- evaluation counter advances exactly once: **PASS**.
- conflict does not overwrite prior project mandate candidate evaluation: **PASS**.
- conflict terminal result cannot be reevaluated: **PASS**.

Denial cases compare before/after counters and existing project 1, mandate 1, candidate 1 and evaluation 1. Role impersonation, duplicate artifact submission, terminal reevaluation, cross-project mandate/parent and repository substitution create no unauthorized record. The successful conflict workflow uses project 2, mandate 2, candidate 5.

### Conflict readback

```json
{
  "candidate_id": 5,
  "state": "OUT_OF_SCOPE",
  "mandate_id": 2,
  "latest_evaluation": "2",
  "baseline_status": "MATCH",
  "candidate_status": "MATCH",
  "evaluation": {
    "caller": "0x686269f09C21aac57f39662855FA51b9758698b2",
    "candidate_id": 5,
    "decision": "OUT_OF_SCOPE",
    "diagnostics": "[{\"classification\":\"FORBIDDEN\",\"mandate_clause\":\"NONE\",\"selector\":\"0x1b55c7e5\"},{\"classification\":\"UNCLEAR\",\"mandate_clause\":\"NONE\",\"selector\":\"0xb6b55f25\"}]",
    "evaluation_id": 2
  }
}
```

Both artifacts MATCH, but forbidden FEE_ROUNDING wins over the exact allowing clause. Authority (not Builder) successfully calls review; caller is recorded. Earlier finalized records remain unchanged. Final counters: 3/3/6/3.

## 6. Preserved earlier ambiguous-mandate attempt

[Raw evidence with inputs/signers/readbacks](LIVE_RUN_V4.json). All rows below reached FINALIZED. Counters are P/M/C/E = projects/mandates/candidates/evaluations. A denial code is a successful contract execution refusing the action, not necessarily a failed blockchain transaction.

| # | Action | Signer | Before → after P/M/C/E | Leader return / consensus | Explorer transaction |
| --- | --- | --- | --- | --- | --- |
| 1 | baseline | Authority | 0/0/0/0 → 1/0/0/0 | Not captured in this suite; outcome independently read back | [0x9b6357297755086cc983c8b5295f0b8d6c8ce35f3618bd7e8583c3c84e26023d](https://explorer-studio.genlayer.com/tx/0x9b6357297755086cc983c8b5295f0b8d6c8ce35f3618bd7e8583c3c84e26023d) |
| 2 | mandate | Authority | 1/0/0/0 → 1/1/0/0 | Not captured in this suite; outcome independently read back | [0x95d0ae13dbfbc0fb5a8a80a36abbe125991da68eea63ad59c77bd6eab83d6f8c](https://explorer-studio.genlayer.com/tx/0x95d0ae13dbfbc0fb5a8a80a36abbe125991da68eea63ad59c77bd6eab83d6f8c) |
| 3 | submit safe | Builder | 1/1/0/0 → 1/1/1/0 | Not captured in this suite; outcome independently read back | [0x909f06e397b82ed7514c0ae9607c00397e4da2e352d94e467f77800fe5a1c6c4](https://explorer-studio.genlayer.com/tx/0x909f06e397b82ed7514c0ae9607c00397e4da2e352d94e467f77800fe5a1c6c4) |
| 4 | evaluate safe | Builder | 1/1/1/0 → 2/1/1/1 | Not captured in this suite; outcome independently read back | [0x5344150b8331610e855df94b9ab2a2798a15493c5ad4e19f5a235d904610bfaa](https://explorer-studio.genlayer.com/tx/0x5344150b8331610e855df94b9ab2a2798a15493c5ad4e19f5a235d904610bfaa) |

The original mandate failed to explicitly authorize the deposit delta. Both artifacts MATCH but the result was REVIEW_REQUIRED. The runner correctly stopped on the failed happy-path expectation; this is retained failed/inconclusive evidence, not rewritten as a success. The exact-mandate suite used a fresh project.

## 7. Production UI and hosting checks

The real production page displayed v4 address. Reload candidate 1 rendered WITHIN_MANDATE, latest_evaluation 1, baseline/candidate MATCH with fetched source/digests. Reload candidate 2 rendered INTEGRITY_FAILURE, hard_reason MISMATCH, latest_evaluation NONE. These matched finalized SDK readbacks.

Connect wallet returned `Error: Install an injected wallet.` in the available in-app browser. No browser-signed transaction or two-wallet account-switching lifecycle was completed. SDK signing is not substituted for that missing proof.

Cloudflare initial v4 deployment: 619e24bc-59bb-41be-9872-26a37cac35f4; index and v4 bundle HTTP 200 and current address/schema confirmed. Subsequent header-only update moved Connect Wallet right, build passed, deployment version be712d85-6937-45e3-855d-4c827e29c2cc (source commit 5d0130b). The earlier bundle record is historical, not the current asset hash. Contract source did not change.

## 8. Reproduce and independently inspect

1. Inspect contract and exact fixture revision above. Confirm current network/address.
2. Run `python -m pytest -q` and `npm run build` locally.
3. Validate saved adversarial receipts with `node verification/check-v4-adversarial.mjs` (read-only, no signing).
4. For fresh live runs, use verification/run-v4.mjs and run-v4-adversarial.mjs with auxiliary keys supplied only through UMS_AUTHORITY_KEY / UMS_BUILDER_KEY; first script also uses UMS_CONTRACT_ADDRESS. These scripts create real records. Do not blindly replay against existing evidence; adversarial runner refuses overwrite. IDs and counters in this report describe the recorded run, not future runs.
5. Open each Explorer TX link and compare captured inputs, signers, successful leader return, agreeing votes and authoritative contract state. The positive suite stores finalized status and readbacks but does not capture full consensus receipts; the adversarial suite does.

## 9. Explicit limitations

- Bounded self-audit, not third-party security audit or proof against every attack.
- Policy conflict tested here is allow-versus-explicit-forbid; forced validator disagreement/NO_MAJORITY is not claimed as passing coverage.
- Browser-signed writes, account switching and pending-to-finalized UI transition remain pending.
- Source/parser scope and model-semantic uncertainty remain as stated above. No claim of real governance adoption, deployed-bytecode equivalence, custody, payout or executed upgrade.
- Historical v2/v3 readiness and source-only claims are superseded by this v4 report.

## 10. Supporting artifacts

- [Exact-mandate lifecycle raw JSON](LIVE_RUN_V4_EXACT_MANDATE.json)
- [Adversarial raw transaction/consensus JSON](LIVE_V4_ADVERSARIAL.json)
- [Earlier ambiguous-mandate raw JSON](LIVE_RUN_V4.json)
- [Deployment/source parity metadata](DEPLOYMENT_V4.json)
- [Browser observation record](BROWSER_V4.md)
- [Steward response and under-1000-character text](MORE_INFORMATION_SUBMIT_V4.md)
