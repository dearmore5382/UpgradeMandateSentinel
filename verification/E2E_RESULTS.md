# StudioNet E2E verification

Date: 2026-10-08. Contract: [`0x9E2E...B1737`](https://explorer-studio.genlayer.com/address/0x9E2Eab87DA372ea3F7E752D146f50D3d323B1737). Identity readback: `UpgradeMandateSentinel`, version `2`, schema `append-only-upgrade-review-v2`.

Two auxiliary wallets executed the workflow. The deployment wallet was not used for any role action. Full before/after counters, signers and post-state are preserved in `LIVE_RUN.json`.

StudioNet returned a transient `ECONNRESET` after the first adversarial submission had finalized. That created candidate `3` but prevented capture of its submit hash. It is not used as evidence. The adversarial case was repeated as candidate `4`, with both submit and evaluation hashes captured; the run then continued from the verified on-chain checkpoint. This explains the otherwise intentional candidate-counter gap in the evidence log.

## Results

- Happy path: safe candidate evaluation finalized as `WITHIN_MANDATE`; diagnostic binds selector `0x22222222` to clause `M-01`. [Evaluation transaction](https://explorer-studio.genlayer.com/tx/0x29c1d89c70e119b03c25776ec44db22f6d272d437c9ba9867f6f6409d9109b5b).
- Role failures: Builder could not publish the mandate, and Authority could not impersonate Builder. Their corresponding counters remained unchanged. [Wrong mandate publisher](https://explorer-studio.genlayer.com/tx/0xf45907030f8860dcacd91a3e895d0e649ff1bb7ac781888164b6d18a3544805b), [wrong candidate publisher](https://explorer-studio.genlayer.com/tx/0x1e111ccbe377b7ebe69566565bdeb1f03b6bb7924c1a24ba295247717187ab26).
- Replay/conflict failures: duplicate artifact, nonexistent parent and cross-project mandate reuse left the candidate counter unchanged. [Replay](https://explorer-studio.genlayer.com/tx/0x97d1524db5273be730a743530162b49b5cf12490ae4364dc8d08e2f3ca802c6f), [invalid parent](https://explorer-studio.genlayer.com/tx/0xa94074e4903c4be9a4ffd10ab925346eff22efbc2d28b1a8a1863de10de2b79a), [cross-project mandate](https://explorer-studio.genlayer.com/tx/0x83e1a539594ab1f15d58a93ebd532e4cdbffa3ce6a810cddcff5f7409270b053).
- Deterministic failure: reordered storage prefix became `HARD_BLOCKED`; attempting evaluation did not append an evaluation. [Storage attack](https://explorer-studio.genlayer.com/tx/0x408d5bb08717c439a30f85c1317d4320cfeb8e470e1dcb342e89c52c930bf510), [rejected evaluation](https://explorer-studio.genlayer.com/tx/0xaea8950a0b948a223610444fd8117123655e1448ba72859e126c32c2243f821e).
- Semantic conflict: added `MINT` capability finalized as `OUT_OF_SCOPE`. [Evaluation transaction](https://explorer-studio.genlayer.com/tx/0x5645c30b1057a2ac0322cb043cedd52898942774c883cbfe19951f37316e1bd6).
- Adversarial audit: prompt-shaped function text plus `ADMIN_REPLACEMENT` could not reach `WITHIN_MANDATE`. [Submit](https://explorer-studio.genlayer.com/tx/0x2620dda6557285c4c9953fd6630dcf2e688791fc13d9fd5702e6d75a9e9fc321), [evaluation](https://explorer-studio.genlayer.com/tx/0x76ee7d7669ed3ac4b299768b2b579000076c82190feba659cb9e384a95ba70f7).
- Correction audit: a child candidate points to rejected candidate `2` and independently finalized as `WITHIN_MANDATE`. [Submit](https://explorer-studio.genlayer.com/tx/0x70075b372716cf58b22c70a177ec32d0e004ead11e782f7948289b59d16c87eb), [evaluation](https://explorer-studio.genlayer.com/tx/0x8eb600cb86d833314c81e3ed65e619b49fd20ae043f33d692451ea1b6d902c81).

## UI/state consistency

The production UI waits for `FINALIZED`, verifies the relevant append-only counter advanced exactly once, then loads the authoritative project, mandate, candidate or evaluation record from the same v2 address. It does not infer success from optional receipt labels. The production build embeds the verified v2 address. Final live counters: projects `2`, mandates `1`, candidates `6`, evaluations `4`. Automated result: **18/18 live checks passed; 9/9 local tests passed; production build passed**.
