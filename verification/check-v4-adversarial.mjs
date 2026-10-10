import {readFileSync} from 'node:fs';
const r=JSON.parse(readFileSync(new URL('./LIVE_V4_ADVERSARIAL.json',import.meta.url)));
const expected={
 'builder cannot publish authority mandate':'AUTHORITY_ONLY',
 'authority cannot impersonate designated builder':'BUILDER_ONLY',
 'duplicate artifact cannot be submitted again':'ARTIFACT_ALREADY_USED',
 'finalized positive cannot be evaluated again':'NOT_REVIEWABLE',
 'integrity failure cannot be evaluated again':'NOT_REVIEWABLE',
 'cross-project mandate binding rejected':'INVALID_BINDING',
 'cross-project parent binding rejected':'INVALID_PARENT',
 'repository substitution rejected':'REPOSITORY_MISMATCH',
 'non-builder reviewer evaluates conflict':'OUT_OF_SCOPE',
 'conflict terminal result cannot be reevaluated':'NOT_REVIEWABLE',
};
if(!r.finished||r.error||r.checks.some(x=>!x.pass))throw Error('Run incomplete or failed');
for(const [label,value] of Object.entries(expected)){
 const t=r.transactions.find(x=>x.label===label);
 if(!t||t.status!=='FINALIZED')throw Error('Missing finalized '+label);
 const leaders=t.receipt.consensus_data.leader_receipt;
 // A trailing idle/cancelled rotation can coexist with the successful quorum.
 const latest=leaders.filter(x=>x.execution_result==='SUCCESS'&&x.result?.status==='return'&&typeof x.result.payload?.readable==='string').at(-1);
 if(!latest)throw Error('No successful readable leader receipt '+label);
 const actual=JSON.parse(latest.result.payload.readable);
 if(latest.execution_result!=='SUCCESS'||actual!==value)throw Error(label+': '+actual);
 const agree=Object.values(t.receipt.consensus_data.votes).filter(x=>x==='agree').length;
 if(agree<3)throw Error('Insufficient captured agreeing votes '+label);
 console.log('PASS',label,value,'agree='+agree);
}
console.log('PASS',r.checks.length,'post-state assertions;',r.transactions.length,'finalized transactions');
