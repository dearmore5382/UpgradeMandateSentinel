# UpgradeMandate Sentinel

UpgradeMandate Sentinel v3 reviews bounded standalone Solidity upgrade artifacts. An Authority registers a baseline locator at a full GitHub commit and a governance mandate; a designated Builder submits candidate locators. Validators fetch manifests and referenced source bytes, recompute their digests and inspect complete manifest/source correspondence. Only matching artifacts proceed to deterministic storage-prefix checks and source-informed mandate assessment. Imports, inheritance, assembly and delegatecall are unsupported and fail closed.

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

The StudioNet v2 deployment `0x9E2Eab87DA372ea3F7E752D146f50D3d323B1737` and its live evidence are historical. They do not verify artifact correspondence and must not be used to claim completion of v3 remediation. Current source is v3 and requires a replacement deployment. See verification/REMEDIATION_V3.md for implementation, verification status and scope.

Live application: https://upgrade-mandate-sentinel.dearmorescheuer5382.workers.dev

## Evidence boundary

This version authenticates who published each canonical manifest and stores its normalized bytes and SHA-256 on-chain. It does **not** claim that a submitted manifest is a complete or canonical Git commit tree. Integrators requiring repository-wide assurance must add a trusted commit-tree attestation before relying on the review receipt.

See [SPEC.md](SPEC.md), [ARCHITECTURE_DIFFERENCE.md](ARCHITECTURE_DIFFERENCE.md), and [verification/TEST_RESOURCE_MANIFEST.json](verification/TEST_RESOURCE_MANIFEST.json).
