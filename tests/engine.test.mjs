import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {compute,PRESETS} from '../site/assets/engine.mjs';
const total=m=>m.flat().reduce((a,b)=>a+b,0);
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
test('two L paths count each turn once and shared endpoints have probability one',()=>{
 const r=compute(PRESETS.diagonal);near(total(r.demand),7);
 near(r.demand[0][0],1);near(r.demand[3][3],1);near(r.demand[3][0],.5);near(r.demand[0][3],.5);near(r.demand[1][1],0);
 near(r.rudyMatched[0][0],7/16);near(r.metrics.total,.8);assert.equal(r.metrics.count,2);
 assert.equal(r.trace.length,2);assert.equal(r.trace[0].cells.length,7);
});
test('straight and same-tile paths collapse without losing endpoint convention',()=>{
 let r=compute(PRESETS.straight);near(total(r.demand),4);for(let x=0;x<4;x++)near(r.demand[x][0],1);
 r=compute(PRESETS.same);near(total(r.demand),1);near(r.demand[0][0],1);near(total(r.rudyMatched),1);near(total(r.rudyRaw),0);
});
test('upstream leg normalization stays a separate two-unit convention',()=>{
 const r=compute(PRESETS.diagonal,{mode:'upstream'});near(total(r.demand),2);near(r.demand[3][0],.25);near(r.demand[0][0],.25);
 near(total(compute(PRESETS.same,{mode:'upstream'}).demand),2);
});
test('reversing net endpoints preserves both distributions',()=>{
 for(const mode of ['path','upstream']) {const a=structuredClone(PRESETS.diagonal),b=structuredClone(a);b.nets[0].reverse();assert.deepEqual(compute(a,{mode}).demand,compute(b,{mode}).demand);}
});
test('RUDY comparison preserves each net mass including zero HPWL cases',()=>{
 for(const data of Object.values(PRESETS))for(const mode of ['path','upstream']){const r=compute(data,{mode});near(total(r.demand),total(r.rudyMatched));}
});
test('rejects invalid capacity, unknown pins and out-of-chip coordinates without mutation',()=>{
 const data=structuredClone(PRESETS.diagonal),before=JSON.stringify(data);compute(data);assert.equal(JSON.stringify(data),before);
 for(const capacity of [0,-1,NaN,Infinity])assert.throws(()=>compute(data,{capacity}),/capacity/);
 data.placement.A.x=99;assert.throws(()=>compute(data),/coordinate/);data.placement.A.x=1;data.nets=[['A','missing']];assert.throws(()=>compute(data),/pin/);
});
test('independent Python agrees on matrices, metrics and boundary cases',()=>{
 const inputs=[];
 for(const data of Object.values(PRESETS))for(const mode of ['path','upstream'])inputs.push({data,mode});
 let seed=73;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32;};
 for(let k=0;k<80;k++){const data=structuredClone(PRESETS.diagonal);for(const p of Object.values(data.placement)){p.x=Math.floor(rnd()*13);p.y=Math.floor(rnd()*13);}inputs.push({data,mode:k%2?'path':'upstream'});}
 const p=spawnSync('python3',['site/downloads/reference.py'],{input:JSON.stringify(inputs),encoding:'utf8'});assert.equal(p.status,0,p.stderr);const output=JSON.parse(p.stdout);
 inputs.forEach((v,i)=>{const js=compute(v.data,{mode:v.mode}),py=output[i];for(const key of ['demand','rudyMatched','rudyRaw'])js[key].flat().forEach((n,j)=>near(n,py[key].flat()[j]));for(const k of ['total','max'])near(js.metrics[k],py.metrics[k]);assert.equal(js.metrics.count,py.metrics.count);});
});
test('helper compatibility reproduces both pinned teacher placement matrices',()=>{
 const audit=JSON.parse(readFileSync(new URL('../docs/research/congestion-upstream-conventions.json',import.meta.url)));
 for(const expected of audit.upstream_conventions.filter(v=>v.model==='probabilistic')){
  const r=compute(PRESETS.teacher,{mode:'upstream',positions:PRESETS.teacher[expected.preset]});r.demand.flat().forEach((v,i)=>near(v,expected.matrix_x_major.flat()[i]));near(r.totalDemand,expected.total_demand);
 }
});
