# Cloudflare v4 deployment

Deployed 2026-10-10 using Wrangler Workers deployment.
URL: https://upgrade-mandate-sentinel.dearmorescheuer5382.workers.dev
Version ID: `619e24bc-59bb-41be-9872-26a37cac35f4`.
Client bundle: `/assets/index-IGxr5-zQ.js`.

Post-deploy HTTP verification: index 200; index references this bundle; bundle 200; bundle contains current contract `0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B` and schema `artifact-bound-upgrade-review-v4`.
Local regression: 19 passed (pytest cache permission warning only). Production build passed outside sandbox; sandbox initially blocked process spawning with EPERM.

These checks establish deployed asset identity, not rendered UI correctness or a browser-signed transaction lifecycle. Those remain pending.
