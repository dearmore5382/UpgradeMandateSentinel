# v4 live lifecycle evidence

Contract: `0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B` (StudioNet).
Deployed source matched repository bytes exactly; SHA-256 `f471a6a4f26ef3c25667a5996b8ea50b1ef8a896e61c3dc37951976e5c961689`.

## Sources and roles

Authored synthetic fixtures (not third-party governance evidence) are pinned to commit `4f91e189810e6e5f266152661de25fba00cb26a2`, under samples/artifacts. The runner separately verifies public HTTP manifest/source bytes and digests.
Authority: `0x686269f09C21aac57f39662855FA51b9758698b2`.
Builder: `0x48CCA889CF67A8420D82341e2fa9532Dc36Ba5c2`.
Deployer signed no workflow transaction. Reviewers can create projects with their own wallets; no deployer allowlist exists.

## Results

[Full transaction hashes, signers, counters and readbacks](LIVE_RUN_V4_EXACT_MANDATE.json): 13 assertions passed, 10 transactions FINALIZED.

| Candidate | Case | Outcome |
| --- | --- | --- |
| 1 | Explicit mandate: preserve deposit, add roundFee | WITHIN_MANDATE; both artifacts MATCH |
| 2 | Manifest omits actual mint | INTEGRITY_FAILURE |
| 3 | Unsupported address storage in source | INTEGRITY_FAILURE; UNSUPPORTED_SOURCE |
| 4 | Zero manifest digest | INTEGRITY_FAILURE; MANIFEST_DIGEST_MISMATCH; evaluation count unchanged |

Happy evaluation transaction: `0xc22edaeb147cb9fec5935d87ddcfdb4e5bbca4edd99e79c23383322e6de46f5f`.
The earlier [ambiguous mandate run](LIVE_RUN_V4.json) is retained: artifacts MATCH but unclear deposit authorization produced REVIEW_REQUIRED. It is not counted as a passing happy path.

## Boundaries and reproduction

Local: `python -m pytest -q` and `npm run build`. Mocked network/model unit tests do not prove live consensus. Live runner: verification/run-v4.mjs, with UMS_CONTRACT_ADDRESS, UMS_AUTHORITY_KEY and UMS_BUILDER_KEY environment variables. It creates new on-chain records; never commit keys.

This evidence establishes SDK-signed lifecycle, not a production browser-signed journey. Production UI/state parity, live conflicting mandates and comprehensive live authorization attacks remain unverified. Review is restricted standalone source analysis, not compiler output, repository-wide attestation, deployed bytecode or proxy execution. Unsupported Solidity fails closed.
