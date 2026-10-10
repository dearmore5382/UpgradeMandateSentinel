import {createClient,createAccount} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionStatus} from 'genlayer-js/types';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
const address='0x2eCb42621DC10023EE0fd1051E7eb119D6bE2B5B';
const file=new URL('./LIVE_V4_ADVERSARIAL.json',import.meta.url);
if(existsSync(file))throw Error('Evidence exists; inspect checkpoint rather than overwrite or blindly replay.');
const a=createAccount(process.env.UMS_AUTHORITY_KEY),b=createAccount(process.env.UMS_BUILDER_KEY);
const reader=createClient({chain:studionet}),aw=createClient({chain:studionet,account:a}),bw=createClient({chain:studionet,account:b});
const out={contract:address,started:new Date().toISOString(),roles:{authority:a.address,builder:b.address},transactions:[],checks:[]};
const save=()=>writeFileSync(file,JSON.stringify(out,null,2)+'\n');
async function retry(fn){for(let i=0;i<8;i++){try{return await fn();}catch(e){if(i===7)throw e;await new Promise(r=>setTimeout(r,2000));}}}
const read=(functionName,args=[])=>retry(()=>reader.readContract({address,functionName,args}));
function check(name,pass,observed){out.checks.push({name,pass,observed});save();if(!pass)throw Error(name);}
const loc=name=>{const path='samples/artifacts/'+name+'.json';return ['dearmore5382','UpgradeMandateSentinel','4f91e189810e6e5f266152661de25fba00cb26a2',path,createHash('sha256').update(readFileSync(new URL('../'+path,import.meta.url))).digest('hex')];};
const snap=async()=>({counts:await read('get_counts'),project:await read('get_project',[1]),mandate:await read('get_mandate',[1]),candidate:await read('get_candidate',[1]),evaluation:await read('get_evaluation',[1])});
async function tx(client,label,functionName,args){const item={label,functionName,args,signer:client===aw?a.address:b.address,before:await read('get_counts'),status:'SUBMITTING'};out.transactions.push(item);save();const response=await client.writeContract({address,functionName,args,value:0n});item.hash=typeof response==='string'?response:response.txId;item.status='SUBMITTED';save();console.log(label,item.hash);await retry(()=>reader.waitForTransactionReceipt({hash:item.hash,status:TransactionStatus.FINALIZED,interval:5000,retries:240}));item.status='FINALIZED';item.receipt=await retry(()=>reader.getTransaction({hash:item.hash}));item.after=await read('get_counts');save();return item;}
async function blocked(client,label,fn,args){const before=await snap();await tx(client,label,fn,args);const after=await snap();check(label,JSON.stringify(before)===JSON.stringify(after),{before,after});}
try{
check('exact v4 identity',(await read('get_contract_version')).version===4,await read('get_contract_version'));
const existing=JSON.parse((await read('get_mandate',[1])).mandate);
await blocked(bw,'builder cannot publish authority mandate','publish_mandate',[1,JSON.stringify(existing)]);
await blocked(aw,'authority cannot impersonate designated builder','submit_candidate',[1,1,'ROOT',...loc('safe')]);
await blocked(bw,'duplicate artifact cannot be submitted again','submit_candidate',[1,1,'ROOT',...loc('safe')]);
await blocked(aw,'finalized positive cannot be evaluated again','evaluate_candidate',[1]);
await blocked(bw,'integrity failure cannot be evaluated again','evaluate_candidate',[2]);
const pid=(await read('get_counts')).project_count;out.conflict_project=pid;save();
await tx(aw,'create isolated conflict project','register_project',['VAULT-2026',b.address,...loc('baseline')]);
const mandate={...existing,mandate_ref:'GOV-V4-CONFLICT',forbidden_capabilities:[...existing.forbidden_capabilities,'FEE_ROUNDING']};
const mid=(await read('get_counts')).mandate_count;out.conflict_mandate=mid;save();await tx(aw,'publish allow-versus-forbid conflict','publish_mandate',[pid,JSON.stringify(mandate)]);
await blocked(bw,'cross-project mandate binding rejected','submit_candidate',[pid,1,'ROOT',...loc('safe')]);
await blocked(bw,'cross-project parent binding rejected','submit_candidate',[pid,mid,'1',...loc('safe')]);
const wrongRepo=loc('safe');wrongRepo[1]='LoanConditionDelta';await blocked(bw,'repository substitution rejected','submit_candidate',[pid,mid,'ROOT',...wrongRepo]);
const cid=(await read('get_counts')).candidate_count;out.conflict_candidate=cid;save();await tx(bw,'builder submits conflicting candidate','submit_candidate',[pid,mid,'ROOT',...loc('safe')]);
const old=await snap();const count=(await read('get_counts')).evaluation_count;
await tx(aw,'non-builder reviewer evaluates conflict','evaluate_candidate',[cid]);
const state=await read('get_candidate',[cid]),checks=await read('get_artifact_checks',[cid]),ev=await read('get_evaluation',[count]);
check('explicit forbidden capability wins over allowing clause',state.state==='OUT_OF_SCOPE'&&checks.baseline.status==='MATCH'&&checks.candidate.status==='MATCH'&&ev.decision==='OUT_OF_SCOPE'&&JSON.parse(ev.diagnostics).some(x=>x.selector==='0x1b55c7e5'&&x.classification==='FORBIDDEN'),{state,checks,ev});
check('evaluation counter advances exactly once',(await read('get_counts')).evaluation_count===count+1,await read('get_counts'));
const now=await snap();check('conflict does not overwrite prior project mandate candidate evaluation',JSON.stringify({...old,counts:null})===JSON.stringify({...now,counts:null}),{before:old,after:now});
await blocked(bw,'conflict terminal result cannot be reevaluated','evaluate_candidate',[cid]);
out.finished=new Date().toISOString();out.final_counts=await read('get_counts');save();console.log('ALL CHECKS PASSED');
}catch(e){out.error=String(e);save();throw e;}
