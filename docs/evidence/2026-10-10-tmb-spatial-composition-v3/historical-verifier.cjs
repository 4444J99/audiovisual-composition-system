#!/usr/bin/env node
/* Bounded acceptance of a locally built edition; writes no source media. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const ADMISSION = path.join(__dirname,'../evidence/2026-10-10-tmb-spatial-composition/edition-receipt.json');
const ADMISSION_SHA256 = '6c41ab26b70e5a80de053ae397917f5dad34c14a33c0efd6a07dae7f940838e7';
const shaBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

function assertAdmission(receipt, admitted) {
  for (const key of ['source_revision','atlas_revision','audio_manifest','generations','audio_provenance']) {
    assert.deepEqual(receipt.source[key],admitted.source[key],`unadmitted source: ${key}`);
  }
  for (const key of ['module','entrypoint','accepted_commit','runtime_graph','release_status']) {
    assert.deepEqual(receipt.engine[key],admitted.engine[key],`unaccepted engine: ${key}`);
  }
  assert.equal(receipt.media.length,admitted.media.length);
  admitted.media.forEach((expected,i)=>{
    for (const [key,value] of Object.entries(expected)) assert.deepEqual(receipt.media[i][key],value,`unadmitted generation ${i}: ${key}`);
  });
  assert.deepEqual(receipt.composition,admitted.composition,'unadmitted composition');
  assert.deepEqual(receipt.preview,admitted.preview,'unadmitted served preview');
}

function assertPoses(observed, direct, count) {
  assert.equal(observed.length,count,'missing rendered panel pose');
  assert.equal(direct.length,count,'missing direct evaluator pose');
  observed.forEach((pose,i)=>{
    for (const field of ['azimuth','elevation','fov']) {
      assert(Number.isFinite(pose[field]) && Number.isFinite(direct[i][field]),`invalid ${field}`);
      assert(Math.abs(pose[field]-direct[i][field])<1e-12,`pose ${i} differs in ${field}`);
    }
  });
}

function assertSignal(samples) {
  for (const id of ['loop-1','loop-2']) for (let channel=0;channel<2;channel++) {
    assert(Math.max(...samples.map(o=>o.levels[id][channel]))>1e-5,`silent ${id} channel ${channel}`);
  }
}

function assertPanEffect(samples, centered) {
  const balance = ([l,r]) => (l*l-r*r)/(l*l+r*r);
  const result = {};
  for (const [id,direction] of [['loop-1',1],['loop-2',-1]]) {
    const differences=samples.map(o=>balance(o.levels[id])-balance(o.rawLevels[id]));
    const effect=differences.reduce((sum,v)=>sum+v,0)/differences.length;
    assert(Number.isFinite(effect),`no measurable panning signal: ${id}`);
    assert(centered ? Math.abs(effect)<.12 : direction*effect>.25,`panning effect missing for ${id}: ${effect}`);
    result[id]=effect;
  }
  return result;
}

function assertResizeContinuity(events) {
  assert(!events.some(e=>['source','seek-command','seeking','seeked','loadstart'].includes(e.type)),
    'orientation caused a media reload or seek');
}

async function verify(edition, playwrightModule, executablePath) {
  const root = fs.realpathSync(edition);
  const preview = path.join(root, 'preview');
  const proofPath = path.join(root, 'browser-acceptance.json');
  const attempts = path.join(root,'browser-acceptance-attempts');
  fs.mkdirSync(attempts,{recursive:true});
  const attemptId=crypto.randomUUID();
  if (fs.existsSync(proofPath)) {
    assert.notEqual(JSON.parse(fs.readFileSync(proofPath)).status,'passed','passed acceptance already exists');
    fs.renameSync(proofPath,path.join(attempts,`legacy-failed-${attemptId}.json`));
  }
  const admissionBytes=fs.readFileSync(ADMISSION);
  assert.equal(shaBytes(admissionBytes),ADMISSION_SHA256,'independent admission was changed');
  const receipt = JSON.parse(fs.readFileSync(path.join(root, 'edition-receipt.json')));
  assertAdmission(receipt,JSON.parse(admissionBytes));
  const plan = JSON.parse(fs.readFileSync(path.join(preview, 'plan.json')));
  const sha = file => shaBytes(fs.readFileSync(file));
  assert.equal(sha(path.join(root, receipt.composition.path)), receipt.composition.sha256);
  for (const item of receipt.media) assert.equal(sha(path.join(root, item.path)), item.sha256);
  assert(receipt.preview.files && Object.keys(receipt.preview.files).length>0, 'missing served-file inventory');
  for (const [relative, expected] of Object.entries(receipt.preview.files)) {
    const target=fs.realpathSync(path.join(preview,relative));
    assert(target.startsWith(preview+path.sep), 'served file escapes preview');
    assert.equal(sha(target),expected,relative);
  }
  for (const source of plan.sources) assert.equal(sha(path.join(preview,source.path)),source.sha256);
  for (const [relative,expected] of Object.entries(receipt.engine.runtime_graph)) {
    assert.equal(sha(path.join(preview,relative)),expected,relative);
  }
  assert.equal(plan.state_sha256,receipt.preview.state_sha256);
  const types = {'.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.mp4':'video/mp4'};
  const server = http.createServer((req, res) => {
    try {
      const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      const target = fs.realpathSync(path.join(preview, relative === '/' ? 'index.html' : relative));
      if (!target.startsWith(preview + path.sep)) {res.writeHead(403).end(); return;}
      const bytes = fs.readFileSync(target);
      const expected=receipt.preview.files[path.relative(preview,target).split(path.sep).join('/')];
      if (!expected || shaBytes(bytes)!==expected) {res.writeHead(409).end();return;}
      res.writeHead(200, {'Content-Type':types[path.extname(target)] || 'application/octet-stream', 'Content-Length':bytes.length});
      res.end(bytes);
    } catch {res.writeHead(404).end();}
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  const observations = [];
  const checks = [];
  const errors = [];
  const proof = {schema:'tmb-composition-browser-acceptance/v1', status:'failed',
    attempt_id:attemptId, admission_sha256:ADMISSION_SHA256, verifier_sha256:sha(__filename),
    created_at:new Date().toISOString(), scope:'real TMB derivatives; headless Chrome; stereo spatial panning',
    edition_receipt_sha256:sha(path.join(root, 'edition-receipt.json')), checks, observations, errors};
  try {
    const {chromium} = require(playwrightModule || 'playwright');
    browser = await chromium.launch({headless:true, executablePath, args:['--disable-dev-shm-usage']});
    proof.browser = browser.version();
    const page = await browser.newPage({viewport:{width:1200,height:800}});
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(`http://127.0.0.1:${server.address().port}/`);
    await page.waitForFunction(() => window.compositionRuntime?.ready, null, {timeout:20000});
    await page.evaluate(() => {
      const r = compositionRuntime, ctx = r.audio.context;
      window.originalNodes = [...r.nodes.values()].map(n => [n.media,n.audio]);
      window.meters = {}; window.rawMeters={};
      function meter(node) {
        const stereo = ctx.createGain(); stereo.channelCount=2; stereo.channelCountMode='explicit';
        const split = ctx.createChannelSplitter(2);
        const a=ctx.createAnalyser(), b=ctx.createAnalyser(); a.fftSize=b.fftSize=2048;
        node.connect(stereo); stereo.connect(split); split.connect(a,0); split.connect(b,1);
        return [a,b];
      }
      for (const n of r.nodes.values()) {
        meters[n.id]=meter(n.audio.gain); rawMeters[n.id]=meter(n.audio.source);
      }
      window.readMeter = map => Object.fromEntries(Object.entries(map).map(([id, pair]) => [id,pair.map(a => {
        const data=new Float32Array(a.fftSize);a.getFloatTimeDomainData(data);
        return Math.sqrt(data.reduce((sum,v)=>sum+v*v,0)/data.length);
      })]));
      window.readLevels=()=>readMeter(meters);
      window.readRawLevels=()=>readMeter(rawMeters);
    });
    await page.click('#stage', {position:{x:4,y:4}});
    await page.waitForFunction(() => compositionRuntime.running && compositionRuntime.snapshot().compositionTime > .6);
    const sample = async name => {
      const observation = await page.evaluate(() => ({snapshot:compositionRuntime.snapshot(), levels:readLevels(),rawLevels:readRawLevels()}));
      observations.push({name,...observation});
      assert.equal(observation.snapshot.error,null);
      assert.equal(observation.snapshot.sharedEngine.error,null);
      assert.equal(observation.snapshot.loops.length,2);
      assert(observation.snapshot.loops.every(n=>n.rate===1),'loop playback rate differs from one');
      return observation;
    };
    const first = await sample('landscape');
    assert.equal(first.snapshot.audio.mode,'spatial_loops');
    assert.equal(first.snapshot.sharedEngine.build,'shared-engine@time-moment-brief/'+receipt.engine.accepted_commit);
    assert.equal(first.snapshot.audio.contextState,'running');
    assert.equal(first.snapshot.loops.length,2);
    assert.notEqual(first.snapshot.loops[0].source,first.snapshot.loops[1].source);
    assert(first.snapshot.loops.every(n=>n.quality.totalVideoFrames>0));
    const phase = (first.snapshot.loops[1].currentTime-first.snapshot.loops[0].currentTime+8)%8;
    assert(Math.abs(phase-1)<.15, `independent one-second phase offset: ${phase}`);
    checks.push('two distinct real sources decode with independent one-second phase offset');
    const direct = await page.evaluate(t => {
      const r=compositionRuntime;
      return SimvltaneaSharedEngineAdapter.createPanelDriver(SharedEngine,{
        panels:r.plan.tracks.length,duration:r.plan.frames/r.plan.fps,sweep:.35,elevation:.12
      }).evaluate(t);
    }, first.snapshot.sharedEngine.renderedTime);
    assertPoses(first.snapshot.sharedEngine.poses,direct,2);
    checks.push('rendered poses equal the accepted shared evaluator');
    for (const loop of first.snapshot.loops) {
      const cell = plan.layout_keyframes[0].layouts.landscape.cells.find(c=>c.loop===loop.id);
      assert(cell, `missing landscape cell for ${loop.id}`);
      const number = v => {const [n,d=1]=String(v).split('/').map(Number);return n/d;};
      const expected = 2*(number(cell.rect[0])+number(cell.rect[2])/2)-1;
      assert(Math.abs(loop.audio.pan-expected)<.002, `pan ${loop.id}`);
    }
    const landscapeSamples=[];
    for (let i=0;i<4;i++) {await page.waitForTimeout(150); landscapeSamples.push(await sample('signal'));}
    assertSignal(landscapeSamples);
    proof.panning={landscape:assertPanEffect(landscapeSamples,false)};
    const eventStart = await page.evaluate(()=>compositionRuntime.events.length);
    await page.setViewportSize({width:600,height:900}); await page.waitForTimeout(350);
    const portrait=await sample('portrait');
    assert(portrait.snapshot.loops.every(n=>Math.abs(n.audio.pan)<.002));
    assert(await page.evaluate(()=>[...compositionRuntime.nodes.values()].every((n,i)=>n.media===originalNodes[i][0]&&n.audio===originalNodes[i][1])));
    const resizeEvents=await page.evaluate(i=>compositionRuntime.events.slice(i),eventStart);
    assertResizeContinuity(resizeEvents);
    const portraitSamples=[];
    for (let i=0;i<4;i++) {await page.waitForTimeout(100);portraitSamples.push(await sample('portrait-signal'));}
    assertSignal(portraitSamples);
    proof.panning.portrait=assertPanEffect(portraitSamples,true);
    checks.push('measured opposing landscape panning and portrait recentering against unpanned source energy');
    checks.push('orientation preserves media/audio nodes and clocks without reload or seek');
    await page.evaluate(()=>compositionRuntime.pause());
    const paused=await sample('paused'); await page.waitForTimeout(250);
    const still=await sample('still-paused');
    assert.equal(paused.snapshot.compositionTime,still.snapshot.compositionTime);
    assert(still.snapshot.loops.every(n=>n.paused));
    assert(Object.values(still.levels).flat().every(v=>v<1e-5));
    await page.click('#stage',{position:{x:4,y:4}});
    await page.waitForFunction(t=>compositionRuntime.snapshot().compositionTime>t+.3,paused.snapshot.compositionTime);
    const resumed=[];
    for (let i=0;i<4;i++) {await page.waitForTimeout(100);resumed.push(await sample('resumed-signal'));}
    assertSignal(resumed);
    checks.push('pause freezes composition and silences audio; gesture resume advances');
    await page.setViewportSize({width:1200,height:800});
    await page.waitForFunction(()=>compositionRuntime.snapshot().compositionTime>8.5,null,{timeout:15000});
    const wrapped=await sample('after-native-wrap');
    assert(wrapped.snapshot.loops.every(n=>!n.paused&&n.currentTime<3&&n.quality.totalVideoFrames>first.snapshot.loops.find(p=>p.id===n.id).quality.totalVideoFrames));
    const wrappedPhase=(wrapped.snapshot.loops[1].currentTime-wrapped.snapshot.loops[0].currentTime+8)%8;
    assert(Math.abs(wrappedPhase-1)<.15, `phase drift after wrap: ${wrappedPhase}`);
    assert(wrapped.snapshot.sharedEngine.poses.every((p,i)=>Math.abs(p.azimuth-first.snapshot.sharedEngine.poses[i].azimuth)>.001));
    checks.push('native eight-second loops wrap with phase preserved and continuing shared poses');
    assert.equal(errors.length,0);
    await page.screenshot({path:path.join(root,'composition-preview.png')});
    proof.events=await page.evaluate(()=>compositionRuntime.events);
    for (const [relative,expected] of Object.entries(receipt.preview.files)) {
      assert.equal(sha(path.join(preview,relative)),expected,`served file changed during verification: ${relative}`);
    }
    checks.push('served media, plan and engine bytes match the edition receipt before and after playback');
    proof.status='passed';
  } catch (e) {proof.failure=String(e); throw e;}
  finally {
    if (browser) await browser.close();
    await new Promise(resolve=>server.close(resolve));
    const attemptPath=path.join(attempts,`${attemptId}.json`);
    fs.writeFileSync(attemptPath,JSON.stringify(proof,null,2)+'\n',{flag:'wx'});
    if (proof.status==='passed') fs.linkSync(attemptPath,proofPath);
  }
  return proof;
}

if (require.main === module) {
  const [edition, playwrightModule, browserPath] = process.argv.slice(2);
  if (!edition || !browserPath) throw new Error('Usage: node verify_tmb_composition.cjs EDITION PLAYWRIGHT_MODULE CHROME_EXECUTABLE');
  const deadline = setTimeout(()=>{console.error('browser verification exceeded 60 seconds');process.exit(124);},60000);
  verify(edition,playwrightModule,browserPath).then(result=>console.log(JSON.stringify({status:result.status,checks:result.checks})))
    .catch(e=>{console.error(e);process.exitCode=1;}).finally(()=>clearTimeout(deadline));
}
module.exports={verify,assertAdmission,assertPoses,assertSignal,assertPanEffect,assertResizeContinuity,ADMISSION,ADMISSION_SHA256};
