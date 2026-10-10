# Production browser verification — 2026-10-10

Environment: Codex in-app browser; actual production page, not an injected mock provider.

Observed through rendered accessibility state:
- Current contract field is 0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B.
- Reload candidate 1 displays WITHIN_MANDATE, latest_evaluation 1, baseline MATCH and candidate MATCH, including fetched source text and exact digests. This matches LIVE_RUN_V4_EXACT_MANDATE.json.
- Reload candidate 2 displays INTEGRITY_FAILURE, hard_reason MISMATCH, latest_evaluation NONE and candidate artifact status MISMATCH. This matches the hidden-mint on-chain readback.
- Connect wallet displays `Error: Install an injected wallet.` No injected wallet is available in the connected browser. No browser-signed transaction was submitted.

Confirmed: rendered happy/hidden-mint readback parity with finalized SDK lifecycle evidence.
Blocked: full two-wallet browser signing journey, including pending-to-finalized transitions and account switching. Requires an accessible browser with the auxiliary wallets connected. Do not substitute mock provider tests or SDK transactions for this proof. Subsequent SDK-signed conflict/authorization controls passed; see ADVERSARIAL_V4.md. They do not remove the browser-signing blocker.
