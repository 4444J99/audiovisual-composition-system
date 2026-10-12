'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const os=require('node:os');
const path=require('node:path');
const http=require('node:http');
const {assertAdmission,assertPoses,assertSignal,assertPanEffect,assertResizeContinuity,
  runAttempt,ADMISSION,ADMISSION_SHA256}=require('../verify_tmb_composition.cjs');

test('independent admission has its pinned digest',()=>{
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(ADMISSION)).digest('hex'),ADMISSION_SHA256);
});
test('mutually consistent alternate media or engine cannot admit itself',()=>{
  const admitted=JSON.parse(fs.readFileSync(ADMISSION));
  assertAdmission(structuredClone(admitted),admitted);
  for (const mutate of [r=>r.media[0].sha256='0'.repeat(64),
    r=>r.engine.accepted_commit='a'.repeat(40),
    r=>r.source.generations[0].audio.sha256='f'.repeat(64),
    r=>r.preview.files['runtime.js']='0'.repeat(64)]) {
    const receipt=structuredClone(admitted); mutate(receipt);
    assert.throws(()=>assertAdmission(receipt,admitted));
  }
});
test('empty, truncated and wrong FOV poses are refused',()=>{
  const direct=[{azimuth:.2,elevation:.3,fov:1},{azimuth:.4,elevation:.1,fov:1}];
  assertPoses(structuredClone(direct),direct,2);
  assert.throws(()=>assertPoses([],direct,2));
  assert.throws(()=>assertPoses(direct.slice(0,1),direct,2));
  const altered=structuredClone(direct); altered[1].fov=2;
  assert.throws(()=>assertPoses(altered,direct,2));
});
test('real channel-energy change is required beyond non-silent stereo',()=>{
  const rawLevels={'loop-1':[1,1],'loop-2':[1,1]};
  const centered={rawLevels,levels:rawLevels};
  const panned={rawLevels,levels:{'loop-1':[2,1],'loop-2':[1,2]}};
  assertPanEffect([panned],false);
  assertPanEffect([centered],true);
  assert.throws(()=>assertPanEffect([centered],false));
  assert.throws(()=>assertPanEffect([panned],true));
});
test('silent resumed voices fail even when their clocks advance',()=>{
  assertSignal([{levels:{'loop-1':[.01,.02],'loop-2':[.02,.01]}}]);
  assert.throws(()=>assertSignal([{levels:{'loop-1':[0,0],'loop-2':[.02,.01]}}]));
});
test('native seeking cannot pass the orientation continuity gate',()=>{
  assertResizeContinuity([{type:'layout'},{type:'audio-pan'}]);
  for (const type of ['source','loadstart','seek-command','seeking','seeked']) {
    assert.throws(()=>assertResizeContinuity([{type}]));
  }
});

function attemptFixture(t) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'composition-attempt-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const proof={attempt_id:crypto.randomUUID(),status:'failed'};
  return {root,proof,canonical:path.join(root,'browser-acceptance.json'),
    attempt:path.join(root,'browser-acceptance-attempts',proof.attempt_id+'.json')};
}

test('successful receipts are independent read-only files',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  let cleaned=false;
  await runAttempt(root,proof,async()=>{proof.status='passed';},async()=>{cleaned=true;});
  assert(cleaned);
  assert.equal(fs.readFileSync(canonical,'utf8'),fs.readFileSync(attempt,'utf8'));
  assert.notEqual(fs.statSync(canonical).ino,fs.statSync(attempt).ino);
  for (const file of [canonical,attempt]) assert.equal(fs.statSync(file).mode&0o222,0);
  const historical=fs.readFileSync(attempt,'utf8');
  fs.chmodSync(canonical,0o644);
  fs.writeFileSync(canonical,'owner changed canonical');
  assert.equal(fs.readFileSync(attempt,'utf8'),historical);
});

test('publication cannot replace an existing canonical receipt',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  fs.writeFileSync(canonical,'retain existing proof');
  await assert.rejects(runAttempt(root,proof,async()=>{proof.status='passed';},async()=>{}),{code:'EEXIST'});
  assert.equal(fs.readFileSync(canonical,'utf8'),'retain existing proof');
  assert.equal(JSON.parse(fs.readFileSync(attempt)).status,'passed');
});

test('deadline failure closes resources and retains a read-only failed attempt',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  const server=http.createServer((req,res)=>res.end('owned test server'));
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  t.after(()=>{server.closeAllConnections();server.close();});
  let aborted=false,cleaned=false;
  await assert.rejects(runAttempt(root,proof,signal=>new Promise(()=>{
    signal.addEventListener('abort',()=>{aborted=true;},{once:true});
  }),async()=>{
    await new Promise(resolve=>server.close(resolve));
    cleaned=true;
  },{timeoutMs:25,cleanupTimeoutMs:500}),{code:'ETIMEDOUT'});
  assert(aborted&&cleaned);
  assert.equal(server.listening,false);
  const recorded=JSON.parse(fs.readFileSync(attempt));
  assert.equal(recorded.status,'failed');
  assert.match(recorded.failure,/exceeded/);
  assert.equal(fs.statSync(attempt).mode&0o222,0);
  assert.equal(fs.existsSync(canonical),false);
});

test('cleanup failures cannot publish passed acceptance',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  await assert.rejects(runAttempt(root,proof,async()=>{proof.status='passed';},async()=>{
    throw new Error('browser close failed');
  }),/browser close failed/);
  const recorded=JSON.parse(fs.readFileSync(attempt));
  assert.equal(recorded.status,'failed');
  assert.match(recorded.cleanup_errors[0],/browser close failed/);
  assert.equal(fs.existsSync(canonical),false);
});

test('hung cleanup is bounded and its failure remains recorded',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  await assert.rejects(runAttempt(root,proof,async()=>{proof.status='passed';},()=>new Promise(()=>{}),
    {timeoutMs:500,cleanupTimeoutMs:25}),/cleanup exceeded/);
  const recorded=JSON.parse(fs.readFileSync(attempt));
  assert.equal(recorded.status,'failed');
  assert.match(recorded.cleanup_errors[0],/cleanup exceeded/);
  assert.equal(fs.existsSync(canonical),false);
});

test('ordinary verification failure retains its cause after cleanup',async t=>{
  const {root,proof,canonical,attempt}=attemptFixture(t);
  let cleaned=false;
  await assert.rejects(runAttempt(root,proof,async()=>{throw new Error('pose mismatch');},async()=>{cleaned=true;}),/pose mismatch/);
  assert(cleaned);
  assert.match(JSON.parse(fs.readFileSync(attempt)).failure,/pose mismatch/);
  assert.equal(fs.existsSync(canonical),false);
});
