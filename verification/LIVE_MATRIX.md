# Required StudioNet verification

| Case | Signer | Expected post-state | Evidence |
|---|---|---|---|
| Preliminary deploy | deployer only | v1 identified; not submission-ready because intended happy fixture failed closed | [contract](https://explorer-studio.genlayer.com/address/0x98D04e3495Ca8E3B4B43Bc8B006f9649c0425D7A), recorded in `DEPLOYMENT.json` |
| Final deploy | deployer only | v2 identity; workflow began from zero counters | [v2 contract](https://explorer-studio.genlayer.com/address/0x9E2Eab87DA372ea3F7E752D146f50D3d323B1737) |
| Register project | Authority auxiliary wallet | authority matches sender | passed; `LIVE_RUN.json` |
| Wrong mandate publisher | Builder wallet | mandate count unchanged | passed; `LIVE_RUN.json` |
| Publish mandate | Authority auxiliary wallet | publisher and project binding match | passed; `LIVE_RUN.json` |
| Wrong candidate publisher | Authority wallet | candidate count unchanged | passed; `LIVE_RUN.json` |
| Safe candidate | Builder auxiliary wallet | `READY_REVIEW` | passed; `LIVE_RUN.json` |
| Safe evaluation | Builder auxiliary wallet | `WITHIN_MANDATE`; selector diagnostic stored | passed; `LIVE_RUN.json` |
| Storage attack | Builder auxiliary wallet | `HARD_BLOCKED`; evaluation count unchanged | passed; `LIVE_RUN.json` |
| Forbidden capability | Builder auxiliary wallet | `OUT_OF_SCOPE` | passed; `LIVE_RUN.json` |
| Adversarial prompt-shaped input | Builder auxiliary wallet | cannot reach `WITHIN_MANDATE` | passed; `LIVE_RUN.json` |
| Artifact replay | Builder wallet | candidate count unchanged | passed; `LIVE_RUN.json` |
| Invalid parent/cross-project mandate | Builder wallet | candidate count unchanged | passed; `LIVE_RUN.json` |
| Correction child | Builder wallet | parent edge points to prior candidate and independently passes | passed; `LIVE_RUN.json` |
| Reviewer self-test | reviewer wallets | fresh independent project lifecycle | reproducible in UI |

Record transaction hash, signer, before/after counters and the corresponding project, mandate, candidate or evaluation readback. Never add fabricated hashes.
