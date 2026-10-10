# Local verification

Historical v2 results. Current v3 results and limitations: REMEDIATION_V3.md.

Date: 2026-10-08.

`python -m pytest -q`: **9 passed** across production contract behavior and frontend guards.

Covered: deployer has no workflow role; authenticated sources; append-only happy review; deterministic storage hard-block without AI; artifact replay; invalid parent; correction lineage; retryable unknown; forbidden cross-field override; persistent normalized diagnostics; project-reference binding; contract identity.

Local mocks are not presented as live-chain evidence. The completed StudioNet lifecycle, finalized transaction hashes, counter transitions and authoritative post-state are recorded separately in `LIVE_RUN.json` and `E2E_RESULTS.md`.

`npm run build`: **passed** with Vite 8.3.3. The only warning is the non-blocking SDK bundle-size advisory.
