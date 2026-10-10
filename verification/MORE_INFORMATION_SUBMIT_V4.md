# Steward remediation mapping

Concern: manifest publisher authentication did not prove correspondence to actual upgrade artifacts.

1. Validators fetch full-commit-pinned manifests and referenced source and recompute both digests.
2. An exhaustive restricted-source parser compares actual selectors/signatures and ordered storage with the complete manifest inventory. Hidden functions and unsupported syntax fail before AI review.
3. Semantic review receives fetched source bodies; uncertainty produces REVIEW_REQUIRED.
4. E2E_V4.md and LIVE_RUN_V4_EXACT_MANDATE.json show finalized positive/negative controls. LIVE_RUN_V4.json preserves the ambiguous-mandate failure.
5. Scope excludes deployed-bytecode attestation and proxy execution. Production signed-browser verification remains pending.

## Response under 1000 characters

Replaced publisher-only review with artifact-bound verification in v4 (0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B). Validators fetch commit-pinned manifests and referenced Solidity source, recompute both digests, and compare actual supported function selectors/signatures and storage with the manifest before semantic review. Hidden functions, unsupported syntax/storage and digest mismatches fail closed. Live auxiliary-wallet tests finalized 10 transactions: the explicit-mandate happy path passed; hidden mint, unsupported storage and bad digest were blocked. The ambiguous-mandate run remains documented as REVIEW_REQUIRED. See verification/E2E_V4.md and LIVE_RUN_V4_EXACT_MANDATE.json. Scope is restricted standalone source review, not deployed-bytecode attestation or upgrade execution. Production signed-browser verification remains pending.
