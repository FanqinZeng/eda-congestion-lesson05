"use strict";
const Placement = (() => {
  // A decimal is an integer coefficient divided by ten to the power scale.
  function parse(value) {
    const match = /^([+-]?)(\d*)(?:\.(\d*))?(?:e([+-]?\d+))?$/i.exec(String(value).trim());
    if (!match || !(match[2] || match[3])) throw Error("decimal");
    let n = BigInt((match[1] || "+") + (match[2] || "") + (match[3] || ""));
    if (n === 0n) return {n, s:0};
    let s = (match[3] || "").length - Number(match[4] || 0);
    if (!Number.isSafeInteger(s)) throw Error("scale");
    if (s < 0) { n *= 10n ** BigInt(-s); s = 0; }
    return {n, s};
  }
  function format({n,s}) {
    if (n === 0n) return "0";
    const sign = n < 0n ? "-" : "";
    let digits = (n < 0n ? -n : n).toString().padStart(s+1,"0");
    if (!s) return sign + digits;
    return sign + (digits.slice(0,-s)+"."+digits.slice(-s)).replace(/0+$/,"").replace(/\.$/,"");
  }
  function add(a,b,subtract=false) {
    const x=parse(a), y=parse(b), s=Math.max(x.s,y.s);
    return format({n:x.n*10n**BigInt(s-x.s)+(subtract?-1n:1n)*y.n*10n**BigInt(s-y.s),s});
  }
  const diff=(a,b)=>add(a,b,true);
  const cmp=(a,b)=>Math.sign(Number(parse(diff(a,b)).n));
  const min=(a,b)=>cmp(a,b)<=0?a:b, max=(a,b)=>cmp(a,b)>=0?a:b;
  const abs=(v)=>v.replace(/^-/,"");
  const closest=(v,points)=>points.reduce((best,p)=>cmp(abs(diff(v,p)),abs(diff(v,best)))<0?p:best);
  const lim={x:"8",y:"6"};
  function coordinate(raw,axis) {
    const v=format(parse(raw));
    if (cmp(v,"-2")<0 || cmp(v,add(lim[axis],"2"))>0) throw Error("range");
    return v;
  }
  function move(origin,axis,delta) {
    return {...origin,[axis]:max("-2",min(add(lim[axis],"2"),add(origin[axis],delta)))};
  }
  function geometry(a,b) {
    const extent=(k,w)=>max("0",diff(add(min(a[k],b[k]),w),max(a[k],b[k])));
    const dx=extent("x","1"), dy=extent("y","2"), x=parse(dx), y=parse(dy);
    const cells=[a,b].map(c=>{
      const row=closest(c.y,["0","2","4"]);
      const site=String(Math.round(Number(c.x)));
      const aligned=[diff(c.x,site),diff(c.y,row)].every(d=>cmp(abs(d),"0.000000001")<=0);
      const inside=cmp(c.x,"0")>=0&&cmp(c.x,"7")<=0&&cmp(c.y,"0")>=0&&cmp(c.y,"4")<=0;
      return {row,aligned,inside};
    });
    return {area:format({n:x.n*y.n,s:x.s+y.s}),overlap:x.n>0n&&y.n>0n,cells};
  }
  // Quantize pointer displacement, with half steps rounded away from zero.
  const dragDelta=d=>String(Math.sign(d)*Math.floor(Math.abs(d)*10+0.5)/10);
  return {coordinate,move,geometry,dragDelta,cmp};
})();
if (typeof module !== "undefined") module.exports=Placement;
