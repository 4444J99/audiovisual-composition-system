'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const crypto=require('node:crypto');
const {assertAdmission,assertPoses,assertSignal,assertPanEffect,assertResizeContinuity,
  ADMISSION,ADMISSION_SHA256}=require('../verify_tmb_composition.cjs');

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
