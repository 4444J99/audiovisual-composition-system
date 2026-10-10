#!/usr/bin/env node
/* Bounded acceptance of a locally built edition; writes no source media. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');

async function verify(edition, playwrightModule, executablePath) {
  const {chromium} = require(playwrightModule || 'playwright');
  const root = fs.realpathSync(edition);
  const preview = path.join(root, 'preview');
  const proofPath = path.join(root, 'browser-acceptance.json');
  assert(!fs.existsSync(proofPath), 'acceptance output already exists');
  const receipt = JSON.parse(fs.readFileSync(path.join(root, 'edition-receipt.json')));
  const plan = JSON.parse(fs.readFileSync(path.join(preview, 'plan.json')));
  const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
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
    created_at:new Date().toISOString(), scope:'real TMB derivatives; headless Chrome; stereo spatial panning',
    edition_receipt_sha256:sha(path.join(root, 'edition-receipt.json')), checks, observations, errors};
  try {
    browser = await chromium.launch({headless:true, executablePath, args:['--disable-dev-shm-usage']});
    proof.browser = browser.version();
    const page = await browser.newPage({viewport:{width:1200,height:800}});
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(`http://127.0.0.1:${server.address().port}/`);
    await page.waitForFunction(() => window.compositionRuntime?.ready, null, {timeout:20000});
    await page.evaluate(() => {
      const r = compositionRuntime, ctx = r.audio.context;
      window.originalNodes = [...r.nodes.values()].map(n => [n.media,n.audio]);
      window.meters = {};
      for (const n of r.nodes.values()) {
        const stereo = ctx.createGain(); stereo.channelCount=2; stereo.channelCountMode='explicit';
        const split = ctx.createChannelSplitter(2);
        const a=ctx.createAnalyser(), b=ctx.createAnalyser(); a.fftSize=b.fftSize=2048;
        n.audio.gain.connect(stereo); stereo.connect(split); split.connect(a,0); split.connect(b,1);
        meters[n.id]=[a,b];
      }
      window.readLevels = () => Object.fromEntries(Object.entries(meters).map(([id, pair]) => [id,pair.map(a => {
        const data=new Float32Array(a.fftSize);a.getFloatTimeDomainData(data);
        return Math.sqrt(data.reduce((sum,v)=>sum+v*v,0)/data.length);
      })]));
    });
    await page.click('#stage', {position:{x:4,y:4}});
    await page.waitForFunction(() => compositionRuntime.running && compositionRuntime.snapshot().compositionTime > .6);
    const sample = async name => {
      const observation = await page.evaluate(() => ({snapshot:compositionRuntime.snapshot(), levels:readLevels()}));
      observations.push({name,...observation});
      assert.equal(observation.snapshot.error,null);
      assert.equal(observation.snapshot.sharedEngine.error,null);
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
    first.snapshot.sharedEngine.poses.forEach((pose,i) => {
      assert(Math.abs(pose.azimuth-direct[i].azimuth)<1e-12);
      assert(Math.abs(pose.elevation-direct[i].elevation)<1e-12);
    });
    checks.push('rendered poses equal the accepted shared evaluator');
    for (const loop of first.snapshot.loops) {
      const cell = plan.layout_keyframes[0].layouts.landscape.cells.find(c=>c.loop===loop.id);
      assert(cell, `missing landscape cell for ${loop.id}`);
      const number = v => {const [n,d=1]=String(v).split('/').map(Number);return n/d;};
      const expected = 2*(number(cell.rect[0])+number(cell.rect[2])/2)-1;
      assert(Math.abs(loop.audio.pan-expected)<.002, `pan ${loop.id}`);
    }
    for (let i=0;i<4;i++) {await page.waitForTimeout(150); await sample('signal');}
    for (const id of ['loop-1','loop-2']) for (let channel=0;channel<2;channel++) {
      assert(Math.max(...observations.map(o=>o.levels[id][channel]))>1e-5, `silent ${id} channel ${channel}`);
    }
    checks.push('both real audio sources emit stereo signal with layout-derived pan');
    const eventStart = await page.evaluate(()=>compositionRuntime.events.length);
    await page.setViewportSize({width:600,height:900}); await page.waitForTimeout(350);
    const portrait=await sample('portrait');
    assert(portrait.snapshot.loops.every(n=>Math.abs(n.audio.pan)<.002));
    assert(await page.evaluate(()=>[...compositionRuntime.nodes.values()].every((n,i)=>n.media===originalNodes[i][0]&&n.audio===originalNodes[i][1])));
    const resizeEvents=await page.evaluate(i=>compositionRuntime.events.slice(i),eventStart);
    assert(!resizeEvents.some(e=>['source','seek-command','loadstart'].includes(e.type)));
    checks.push('orientation preserves media/audio nodes and clocks without reload or seek');
    await page.evaluate(()=>compositionRuntime.pause());
    const paused=await sample('paused'); await page.waitForTimeout(250);
    const still=await sample('still-paused');
    assert.equal(paused.snapshot.compositionTime,still.snapshot.compositionTime);
    assert(still.snapshot.loops.every(n=>n.paused));
    assert(Object.values(still.levels).flat().every(v=>v<1e-5));
    await page.click('#stage',{position:{x:4,y:4}});
    await page.waitForFunction(t=>compositionRuntime.snapshot().compositionTime>t+.3,paused.snapshot.compositionTime);
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
    fs.writeFileSync(proofPath,JSON.stringify(proof,null,2)+'\n',{flag:'wx'});
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
module.exports={verify};
