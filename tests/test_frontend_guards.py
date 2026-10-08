from pathlib import Path
SOURCE=(Path(__file__).resolve().parents[1]/"src"/"main.tsx").read_text(encoding="utf-8")
CSS=(Path(__file__).resolve().parents[1]/"src"/"styles.css").read_text(encoding="utf-8")
def test_finality_and_authoritative_append_only_readback():
    assert "status:TransactionStatus.FINALIZED" in SOURCE
    assert "expected append-only counter did not advance" in SOURCE
    assert "receipt.resultName" not in SOURCE
    assert 'typeof v==="string"?JSON.parse(v):v' in SOURCE
def test_contract_identity_and_explorer_are_visible():
    assert 'UpgradeMandateSentinel v2 is required' in SOURCE
    assert 'explorer-studio.genlayer.com/tx/' in SOURCE
    assert 'ACTIVE CONTRACT' in SOURCE
def test_ui_is_a_distinct_three_pane_review_cockpit():
    for label in ("BASELINE","MANDATE","CANDIDATE","CONSENSUS REVIEW","Evaluation trace"):assert label in SOURCE
    assert 'grid-template-columns:repeat(3,1fr)' in CSS
    assert 'upgrade-sentinel-logo.png' in SOURCE
