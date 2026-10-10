# Artifact correspondence remediation

Superseded by REMEDIATION_V4.md after v3 live correspondence returned UNCLEAR/NO_MAJORITY. The implementation and local results below describe v3 history.

Status: local implementation and fixtures prepared; replacement deployment and live consensus verification pending. The previous v2 deployment and 18-check lifecycle establish publisher authentication only and do not prove artifact correspondence.

Steward concern: manifests are signed by publishers but are not established as descriptions of referenced upgrade artifacts.

Invariant: no candidate may reach WITHIN_MANDATE unless validators independently fetch both baseline and candidate manifests and their referenced Solidity source at full GitHub commit SHA, recompute both manifest and source SHA-256 digests, and agree that each manifest completely corresponds to its source. Mandate assessment receives the verified source bodies in addition to selector/signature/capability changes. Changing source bytes triggers review even if declared signatures remain identical.

The contract constructs URLs on raw.githubusercontent.com from validated components. Source is bounded to 24,000 bytes; manifests to 12,000 bytes. Imports, inheritance, assembly and delegatecall are unsupported and fail closed. Semantic correspondence checks actual bodies, public getters and omitted externally callable functions, plus ordered storage declarations. Source fetch failures and UNCLEAR remain retryable; digest failures, correspondence MISMATCH and unsupported source cannot create a positive evaluation. get_artifact_checks exposes observed digests, source bodies and correspondence outcomes for both artifacts.

Regression mapping:

| Requirement | Local verification | Required live verification |
|---|---|---|
| Recompute manifest digest | substituted bytes are rejected before model | bad committed digest leaves no positive state |
| Recompute source digest | correct manifest hash with wrong source bytes rejected | source mismatch negative control |
| Correspondence | production observation called with complete source; model result gate tested | hidden-mint.json and wrong-storage.json must fail with valid digests |
| Recovery | unavailable/unclear retries through evaluate_candidate | unavailable source remains REVIEW_REQUIRED |
| Source context | fetched source passed to mandate review | happy source reaches WITHIN_MANDATE |
| UI | v3 identity and branch-specific authoritative readback | signed production browser journey on replacement address |

Local results: 18 tests passed on 2026-10-10; production build passed. Network and model responses in local tests are mocked. This is not live evidence of model accuracy or validator consensus. v3 StudioNet evidence remains pending.

Scope: a receipt reviews the exact bounded source file supplied at the pinned revision. It does not certify a complete repository, compiler output, deployed proxy implementation, bytecode equivalence, or real-world governance legitimacy. A project registrant is the authority for that project; the deployer receives no role. Solidity fixtures are intentionally synthetic test artifacts and not production vault contracts.

Resubmit text must only claim deployment, consensus negative controls and production journey after those have completed. Required new address: UpgradeMandateSentinel version 3, schema artifact-bound-upgrade-review-v3.
