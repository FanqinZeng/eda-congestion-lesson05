const assert=require("node:assert/strict");
const m=require("./model.js");
const p=(x,y)=>({x,y});
const a=p("2.35","1.02"), b=p("4","2");
for(const [delta,expected] of [["0.1","2.45"],[m.dragDelta(0.5),"2.85"]]){
  const next=m.move(a,"x",delta);
  assert.deepEqual(next,p(expected,"1.02"));
  assert.equal(m.geometry(next,b).cells[0].row,"2");
}
for(const [x,area] of [["2","0"],["1.9999999995","0.000000001"],["2.0000000005","0"]]){
  const result=m.geometry(p("1","0"),p(x,"0"));
  assert.equal(result.area,area);
  assert.equal(result.overlap,area!=="0");
}
assert.equal(m.coordinate("2.350000000000000000001","x"),"2.350000000000000000001");
console.log("model fixtures OK");
