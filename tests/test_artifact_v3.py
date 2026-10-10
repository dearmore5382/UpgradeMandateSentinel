import json,hashlib
from unittest.mock import patch
import pytest
from types import SimpleNamespace
from historical_v2_support import deploy,sync,eth
SHA='a'*40
def setup(vm,c,a,b):
    with vm.prank(a):
        sync(vm,c);p=c.register_project('VAULT',eth(b),'owner','repo',SHA,'base.json','1'*64)
        m=c.publish_mandate(p,json.dumps({'schema':'upgrade-mandate-v1','project_ref':'VAULT','mandate_ref':'GOV','clauses':[{'clause_id':'M1','allowed_change':'Add roundFee(uint256).'}],'forbidden_capabilities':['MINT']}))
    with vm.prank(b):sync(vm,c);cid=c.submit_candidate(p,m,'ROOT','owner','repo',SHA,'candidate.json','2'*64)
    return cid
def obs(status='MATCH',extra=False,slots=None):
    fs=[{'selector':'0x11111111','signature':'deposit(uint256)','capability':'DEPOSIT'}]
    if extra:fs.append({'selector':'0x22222222','signature':'roundFee(uint256)','capability':'FEE_ROUNDING'})
    return {'status':status,'manifest_sha256':'1'*64,'source_sha256':'3'*64,'manifest':json.dumps({'schema':'upgrade-manifest-v2','project_ref':'VAULT','source_path':'Vault.sol','source_sha256':'3'*64,'functions':fs,'storage':slots or [{'slot':0,'label':'balance','type':'uint256'}]})}
def evaluate(vm,c,cid,base,head):
    mod=c._instance.register_project.__globals__;calls=iter([base,head])
    with vm.activate(),patch.dict(mod,{'_artifact_verify':lambda *_:next(calls),'_review':lambda *_:{'decision':'WITHIN_MANDATE','labels':[{'selector':'0x22222222','classification':'ALLOWED','mandate_clause':'M1'}]}}):sync(vm,c);return c.evaluate_candidate(cid)
def test_authenticated_happy_path():
    vm,c,a,b=deploy();cid=setup(vm,c,a,b)
    assert evaluate(vm,c,cid,obs(),obs(extra=True))=='WITHIN_MANDATE'
    assert c.get_evaluation(0)['candidate_id']==cid
@pytest.mark.parametrize('status',['MANIFEST_DIGEST_MISMATCH','SOURCE_DIGEST_MISMATCH','MISMATCH','UNSUPPORTED_SOURCE'])
def test_artifact_failure_blocks_positive_even_when_mandate_model_allows(status):
    vm,c,a,b=deploy();cid=setup(vm,c,a,b)
    assert evaluate(vm,c,cid,obs(),obs(status,True))=='INTEGRITY_FAILURE'
    assert c.get_counts()['evaluation_count']==0;assert c.get_candidate(cid)['hard_reason']==status
@pytest.mark.parametrize('status',['SOURCE_UNAVAILABLE','UNCLEAR'])
def test_retryable_source_failure(status):
    vm,c,a,b=deploy();cid=setup(vm,c,a,b)
    assert evaluate(vm,c,cid,obs(),obs(status,True))=='REVIEW_REQUIRED'
    assert c.get_counts()['evaluation_count']==0
    assert evaluate(vm,c,cid,obs(),obs(extra=True))=='WITHIN_MANDATE'
def test_storage_hard_block():
    vm,c,a,b=deploy();cid=setup(vm,c,a,b)
    assert evaluate(vm,c,cid,obs(),obs(extra=True,slots=[{'slot':0,'label':'owner','type':'address'}]))=='HARD_BLOCKED'
    assert c.get_counts()['evaluation_count']==0
def test_recompute_actual_manifest_bytes():
    _,c,_,_=deploy();mod=c._instance.register_project.__globals__
    with patch.dict(mod,{'_fetch':lambda *_:b'substituted bytes'}):result=mod['_artifact_observe']('owner','repo',SHA,'base.json','1'*64,'VAULT')
    assert result['status']=='MANIFEST_DIGEST_MISMATCH';assert result['manifest_sha256']==hashlib.sha256(b'substituted bytes').hexdigest()
def test_clause_required():
    _,c,_,_=deploy();mod=c._instance.register_project.__globals__
    assert mod['_normalize']({'decision':'WITHIN_MANDATE','labels':[{'selector':'0x22222222','classification':'ALLOWED','mandate_clause':'NONE'}]},[{'selector':'0x22222222'}],['M1'])['decision']=='REVIEW_REQUIRED'

@pytest.mark.parametrize('fixture,model_answer,expected',[('safe','MATCH','MATCH'),('hidden-mint','MISMATCH','MISMATCH'),('wrong-storage','MISMATCH','MISMATCH'),('safe','garbage','UNCLEAR')])
def test_observation_fetches_exact_source_and_uses_correspondence_model(fixture,model_answer,expected):
    from pathlib import Path
    _,c,_,_=deploy();mod=c._instance.register_project.__globals__;folder=Path(__file__).resolve().parents[1]/'samples'/'artifacts';raw=(folder/(fixture+'.json')).read_bytes();value=json.loads(raw);source=(folder/value['source_path'].split('/')[-1]).read_bytes();seen=[]
    def fetch(url,limit):seen.append(url);return raw if url.endswith('.json') else source
    prompts=[]
    def prompt(text,**kwargs):prompts.append(text);return {'correspondence':model_answer}
    fake=SimpleNamespace(nondet=SimpleNamespace(exec_prompt=prompt))
    with patch.dict(mod,{'_fetch':fetch,'gl':fake}):result=mod['_artifact_observe']('owner','repo',SHA,'samples/artifacts/'+fixture+'.json',hashlib.sha256(raw).hexdigest(),'VAULT-2026')
    assert result['status']==('UNSUPPORTED_SOURCE' if fixture=='wrong-storage' else expected);assert result['source_sha256']==hashlib.sha256(source).hexdigest();assert len(seen)==2
    if fixture=='safe':assert source.decode() in prompts[0]
    else:assert prompts==[], 'Structural omission/storage failure must be detected without AI'

def test_actual_selector_and_complete_inventory():
    from pathlib import Path
    _,c,_,_=deploy();mod=c._instance.register_project.__globals__;folder=Path(__file__).resolve().parents[1]/'samples'/'artifacts'
    parsed=mod['_source_structure']((folder/'Safe.sol').read_text())
    assert parsed['functions']==[{'selector':'0x1b55c7e5','signature':'roundFee(uint256)'},{'selector':'0xb6b55f25','signature':'deposit(uint256)'}]
    assert len(mod['_source_structure']((folder/'HiddenMint.sol').read_text())['functions'])==3
    with pytest.raises(ValueError):mod['_source_structure']('pragma solidity ^0.8.24; contract X { import "evil.sol"; }')

def test_correct_manifest_digest_wrong_source_bytes_never_calls_model():
    from pathlib import Path
    _,c,_,_=deploy();mod=c._instance.register_project.__globals__;raw=(Path(__file__).resolve().parents[1]/'samples'/'artifacts'/'safe.json').read_bytes()
    def fetch(url,limit):return raw if url.endswith('.json') else b'wrong source'
    fake=SimpleNamespace(nondet=SimpleNamespace(exec_prompt=lambda *_:pytest.fail('Model must not run before digest verification')))
    with patch.dict(mod,{'_fetch':fetch,'gl':fake}):result=mod['_artifact_observe']('owner','repo',SHA,'safe.json',hashlib.sha256(raw).hexdigest(),'VAULT-2026')
    assert result['status']=='SOURCE_DIGEST_MISMATCH'
