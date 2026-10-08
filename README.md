# UpgradeMandate Sentinel

UpgradeMandate Sentinel is a source-bound GenLayer review primitive for proxy upgrades. A Project Authority registers a canonical baseline manifest and governance mandate; a designated Builder submits immutable candidate nodes; deterministic layout checks hard-block unsafe storage changes; GenLayer consensus classifies remaining capability deltas against the mandate.

The contract does not execute an upgrade. It produces an auditable review receipt for downstream timelocks or upgrade executors.

## Roles

- **Deployer:** deploys only and receives no workflow privilege.
- **Project Authority:** the sender that registers a project; publishes that project's mandates.
- **Builder:** address designated by the Project Authority; submits candidates.
- **Reviewer:** any wallet may call evaluation.

A reviewer can create a fresh project with wallets they control. There is no deployer allowlist.

## Run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
npm install
npm run build
npm run dev
```

Deploy `contracts/UpgradeMandateSentinel.py` on StudioNet and enter the deployment address in the cockpit. Never commit private keys or API tokens.

Submission-ready StudioNet v2 deployment: `0x9E2Eab87DA372ea3F7E752D146f50D3d323B1737`. The first v1 deployment is retained only as preliminary fail-closed evidence and must not be submitted.

Live application: https://upgrade-mandate-sentinel.dearmorescheuer5382.workers.dev

## Evidence boundary

This version authenticates who published each canonical manifest and stores its normalized bytes and SHA-256 on-chain. It does **not** claim that a submitted manifest is a complete or canonical Git commit tree. Integrators requiring repository-wide assurance must add a trusted commit-tree attestation before relying on the review receipt.

See [SPEC.md](SPEC.md), [ARCHITECTURE_DIFFERENCE.md](ARCHITECTURE_DIFFERENCE.md), and [verification/TEST_RESOURCE_MANIFEST.json](verification/TEST_RESOURCE_MANIFEST.json).
