/** Pure GCell engine. Matrices are x-major: matrix[column][row], y increases up. */
import teacher from './teacher.mjs';
const clone=x=>JSON.parse(JSON.stringify(x));
const base={chip:{W:12,H:12},gcell:{nx:4,ny:4,cellW:3,cellH:3},capacity:.6,nets:[['A','B']],placement:{A:{x:1,y:1},B:{x:10,y:10}}};
export const PRESETS={diagonal:clone(base),straight:{...clone(base),placement:{A:{x:1,y:1},B:{x:10,y:1}}},same:{...clone(base),placement:{A:{x:1,y:1},B:{x:1,y:1}}},multi:{...clone(base),nets:[['A','B','C']],placement:{A:{x:1,y:1},B:{x:10,y:1},C:{x:10,y:10}}},teacher};
export const zeros=(nx,ny)=>Array.from({length:nx},()=>Array(ny).fill(0));
const range=(a,b)=>Array.from({length:Math.abs(b-a)+1},(_,i)=>a+i*(b>=a?1:-1));
const unique=cells=>[...new Map(cells.map(p=>[p.join(','),p])).values()];
export function routeCells(a,b,order='HV'){
 const bend=order==='HV'?[b[0],a[1]]:[a[0],b[1]];
 const line=(p,q)=>p[1]===q[1]?range(p[0],q[0]).map(i=>[i,p[1]]):range(p[1],q[1]).map(j=>[p[0],j]);
 const legs=[line(a,bend),line(bend,b)];return {bend,legs,cells:unique(legs.flat())};
}
export function metrics(matrix,capacity){let total=0,max=0,count=0;for(const d of matrix.flat()){const o=Math.max(0,d-capacity);total+=o;max=Math.max(max,o);if(o>1e-12)count++;}return {total,max,count};}
export function compute(data,{mode='path',capacity=data.capacity,positions=data.placement}={}){
 if(!['path','upstream'].includes(mode))throw Error('mode');
 if(!Number.isFinite(capacity)||capacity<=0)throw Error('capacity must be finite and positive');
 const {nx,ny,cellW:cw,cellH:ch}=data.gcell;
 if(!Number.isInteger(nx)||!Number.isInteger(ny)||nx<1||ny<1||nx>32||ny>32||cw<=0||ch<=0)throw Error('grid');
 for(const p of Object.values(positions))if(!Number.isFinite(p.x)||!Number.isFinite(p.y)||p.x<0||p.y<0||p.x>data.chip.W||p.y>data.chip.H)throw Error('coordinate outside chip');
 const tile=p=>[Math.max(0,Math.min(nx-1,Math.floor(p.x/cw))),Math.max(0,Math.min(ny-1,Math.floor(p.y/ch)))];
 const demand=zeros(nx,ny),rudyRaw=zeros(nx,ny),rudyMatched=zeros(nx,ny),trace=[];
 for(const [netIndex,net] of data.nets.entries()){
  if(net.some(id=>!positions[id])||new Set(net).size!==net.length||net.length<2)throw Error('net requires distinct known pins');
  const pins=net.map(id=>positions[id]),xs=pins.map(p=>p.x),ys=pins.map(p=>p.y);
  const lo={x:Math.min(...xs),y:Math.min(...ys)},hi={x:Math.max(...xs),y:Math.max(...ys)},center={x:(lo.x+hi.x)/2,y:(lo.y+hi.y)/2};
  const edges=net.length===2?[[pins[0],pins[1],1]]:pins.map(p=>[center,p,1/net.length]);let mass=0;
  for(const [edgeIndex,[a,b,scale]] of edges.entries())for(const order of ['HV','VH']){
   const path=routeCells(tile(a),tile(b),order),deposits=[];
   if(mode==='path')for(const [i,j] of path.cells)deposits.push({i,j,value:.5*scale});
   else for(const leg of path.legs)for(const [i,j] of leg)deposits.push({i,j,value:.5*scale/leg.length});
   for(const {i,j,value} of deposits){demand[i][j]+=value;mass+=value;}
   trace.push({id:`n${netIndex}-e${edgeIndex}-${order}`,netIndex,edgeIndex,net:[...net],order,a:tile(a),b:tile(b),bend:path.bend,cells:path.cells,legs:path.legs,deposits,scale,probability:.5,cumulative:clone(demand)});
  }
  const [i0,j0]=tile(lo),[i1,j1]=tile(hi),tiles=[];for(let i=i0;i<=i1;i++)for(let j=j0;j<=j1;j++)tiles.push([i,j]);
  const hpwl=hi.x-lo.x+hi.y-lo.y;
  for(const [i,j] of tiles){rudyRaw[i][j]+=hpwl/tiles.length;rudyMatched[i][j]+=mass/tiles.length;}
 }
 return {nx,ny,mode,capacity,demand,rudyRaw,rudyMatched,trace,metrics:metrics(demand,capacity),rudyMetrics:metrics(rudyMatched,capacity),totalDemand:demand.flat().reduce((a,b)=>a+b,0)};
}
