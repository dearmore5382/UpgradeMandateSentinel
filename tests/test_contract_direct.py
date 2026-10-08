from pathlib import Path
import importlib,json,sys
from unittest.mock import patch
from gltest.direct import VMContext,create_address,deploy_contract
ROOT=Path(__file__).resolve().parents[1];FILE=ROOT/'contracts'/'UpgradeMandateSentinel.py'
def eth(x):
    if isinstance(x,bytes):return '0x'+bytes(x).hex()
    x=str(x);return '0x'+x[5:] if x.startswith('addr#') else x
def manifest(ref='VAULT-2026',artifact='11'*32,storage=None,extra=None):
    fs=[{'selector':'0x11111111','signature':'deposit(uint256)','capability':'DEPOSIT'}]
    if extra:fs+=extra
    return json.dumps({'schema':'upgrade-manifest-v1','project_ref':ref,'artifact_sha256':artifact,'functions':fs,'storage':storage if storage is not None else [{'slot':0,'label':'owner','type':'address'},{'slot':1,'label':'balance','type':'uint256'}]},separators=(',',':'))
def mandate(ref='VAULT-2026'):
    return json.dumps({'schema':'upgrade-mandate-v1','project_ref':ref,'mandate_ref':'GOV-42','clauses':[{'clause_id':'M-01','allowed_change':'Add bounded fee rounding helper.'}],'forbidden_capabilities':['MINT','ARBITRARY_WITHDRAW','ADMIN_REPLACEMENT']},separators=(',',':'))
def deploy():
    authority,builder=create_address('authority'),create_address('builder');vm=VMContext(create_address('deployer'))
    with patch('os.unlink',lambda _:None),vm.activate():
        c=deploy_contract(FILE,vm);g=c._instance.register_project.__globals__['gl'];_=g.nondet;_=g.vm
    sdk=str(Path(g._cached_gl.__file__).resolve().parents[2]);sys.path.insert(0,sdk) if sdk not in sys.path else None;importlib.import_module('genlayer');return vm,c,authority,builder
def sync(vm,c):
    g=c._instance.register_project.__globals__['gl'];s=vm.sender;s=type(g.message.sender_address)(s) if isinstance(s,bytes) else s;g._cached_gl.message=g.message._replace(sender_address=s,origin_address=s,value=type(g.message.value)(vm.value));g._cached_gl.message_raw['sender_address']=s;g._cached_gl.message_raw['origin_address']=s
def setup(vm,c,a,b):
    with vm.prank(a):sync(vm,c);p=c.register_project('VAULT-2026',eth(b),manifest());m=c.publish_mandate(p,mandate())
    return p,m
def test_deployer_has_no_role_and_happy_append_only_review():
    vm,c,a,b=deploy();p,m=setup(vm,c,a,b);extra=[{'selector':'0x22222222','signature':'roundFee(uint256)','capability':'FEE_ROUNDING'}]
    with vm.activate():sync(vm,c);assert c.submit_candidate(p,m,'ROOT',manifest(artifact='22'*32,extra=extra))=='BUILDER_ONLY'
    with vm.prank(b):sync(vm,c);cid=c.submit_candidate(p,m,'ROOT',manifest(artifact='22'*32,extra=extra))
    mod=c._instance.register_project.__globals__;ok={'decision':'WITHIN_MANDATE','labels':[{'selector':'0x22222222','classification':'ALLOWED','mandate_clause':'M-01'}]}
    with vm.activate(),patch.dict(mod,{'_review':lambda *_:ok}):sync(vm,c);assert c.evaluate_candidate(cid)=='WITHIN_MANDATE'
    assert c.get_candidate(cid)['state']=='WITHIN_MANDATE';assert c.get_evaluation(0)['candidate_id']==cid
def test_storage_change_is_deterministically_hard_blocked_without_ai():
    vm,c,a,b=deploy();p,m=setup(vm,c,a,b);bad=[{'slot':0,'label':'balance','type':'uint256'},{'slot':1,'label':'owner','type':'address'}]
    with vm.prank(b):sync(vm,c);cid=c.submit_candidate(p,m,'ROOT',manifest(artifact='33'*32,storage=bad))
    assert c.get_candidate(cid)['state']=='HARD_BLOCKED';assert c.get_candidate(cid)['hard_reason']=='STORAGE_PREFIX_CHANGED';assert c.evaluate_candidate(cid)=='HARD_BLOCKED';assert c.get_counts()['evaluation_count']==0
def test_artifact_replay_parent_and_mandate_binding():
    vm,c,a,b=deploy();p,m=setup(vm,c,a,b)
    with vm.prank(b):sync(vm,c);cid=c.submit_candidate(p,m,'ROOT',manifest(artifact='44'*32));assert c.submit_candidate(p,m,'ROOT',manifest(artifact='44'*32))=='ARTIFACT_ALREADY_USED';assert c.submit_candidate(p,m,'999',manifest(artifact='55'*32))=='INVALID_PARENT';child=c.submit_candidate(p,m,str(cid),manifest(artifact='66'*32))
    assert c.get_candidate(child)['parent_candidate']==str(cid)
def test_unknown_is_retryable_and_diagnostics_persist():
    vm,c,a,b=deploy();p,m=setup(vm,c,a,b);extra=[{'selector':'0x33333333','signature':'mystery(bytes)','capability':'UNKNOWN_POWER'}]
    with vm.prank(b):sync(vm,c);cid=c.submit_candidate(p,m,'ROOT',manifest(artifact='77'*32,extra=extra))
    mod=c._instance.register_project.__globals__;u={'decision':'REVIEW_REQUIRED','labels':[{'selector':'0x33333333','classification':'UNCLEAR','mandate_clause':'NONE'}]};deny={'decision':'OUT_OF_SCOPE','labels':[{'selector':'0x33333333','classification':'FORBIDDEN','mandate_clause':'NONE'}]}
    with vm.activate(),patch.dict(mod,{'_review':lambda *_:u}):sync(vm,c);assert c.evaluate_candidate(cid)=='REVIEW_REQUIRED'
    with vm.activate(),patch.dict(mod,{'_review':lambda *_:deny}):sync(vm,c);assert c.evaluate_candidate(cid)=='OUT_OF_SCOPE'
    assert c.get_counts()['evaluation_count']==2;assert 'FORBIDDEN' in c.get_evaluation(1)['diagnostics']
def test_normalizer_forces_cross_field_decision():
    _,c,_,_=deploy();m=c._instance.register_project.__globals__;ds=[{'selector':'0xaaaaaaaa','change':'ADDED','before_capability':'NONE','after_capability':'MINT','before_signature':'NONE','after_signature':'mint(address,uint256)'}]
    r=m['_normalize']({'decision':'WITHIN_MANDATE','labels':[{'selector':'0xaaaaaaaa','classification':'FORBIDDEN','mandate_clause':'NONE'}]},ds,['M-01']);assert r['decision']=='OUT_OF_SCOPE'
def test_source_binding_and_contract_identity():
    vm,c,a,b=deploy();p,m=setup(vm,c,a,b)
    with vm.prank(b):sync(vm,c);assert c.submit_candidate(p,m,'ROOT',manifest(ref='OTHER',artifact='88'*32))=='INVALID_CANDIDATE'
    assert c.get_contract_version()=={'name':'UpgradeMandateSentinel','version':2,'schema':'append-only-upgrade-review-v2'};assert c.get_project(p)['authority'].lower()==eth(a).lower()
