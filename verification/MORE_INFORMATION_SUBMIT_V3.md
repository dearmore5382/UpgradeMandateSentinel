# Resubmission preparation

Status: DRAFT — do not submit until v3 live verification completes.

The steward requested proof that authenticated manifests correspond to their referenced upgrade artifacts. v3 replaces caller-supplied manifest content with full-commit GitHub locators. Validators fetch manifests and their referenced source files, recompute their SHA-256 digests, and check complete function/capability/storage correspondence before mandate review. Source bodies also enter mandate assessment. Digest mismatch and misleading manifests block positive decisions; unavailable or inconclusive sources remain retryable. Artifact observations are readable through get_artifact_checks. New negative controls contain valid hashes but hide minting or misstate storage.

Pending proof: exact v3 deployment address and source parity; finalized happy, hidden-mint, wrong-storage, digest mismatch and unavailable-source transactions; production UI signed journey. Local result: 18 tests and production build passed with mocked external dependencies. No claim is made that v2 evidence covers these requirements.
