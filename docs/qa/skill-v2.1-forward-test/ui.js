"use strict";
const by=id=>document.getElementById(id);
const copy={
  zh:["微型布局实验","拖动单元，或聚焦单元后按方向键，每次移动 0.1。坐标为左下角。","重置","相交面积","最近行","合法","是","否","请输入范围内的有限小数","两个单元左下角为 (1,0) 和 (1.75,0) 时，相交面积是多少？","核对","正确，0.25 × 2 = 0.5。","再试一次。共同宽度为 0.25，高度为 2。","阅读 Python 参考","下载示例"],
  en:["Mini Placement","Drag a cell or focus it and press an arrow to move by 0.1. Coordinates mark its lower-left corner.","Reset","Overlap area","Nearest row","Legal","yes","no","Enter a finite decimal within range","What is the overlap area for cells at (1,0) and (1.75,0)?","Check","Correct. 0.25 × 2 = 0.5.","Try again. The shared width is 0.25 and the height is 2.","Read Python reference","Download example"]
};
let language=new URL(location.href).searchParams.get("lang")==="en"?"en":"zh";
const initial={A:{x:"2.35",y:"1.02"},B:{x:"4",y:"2"}};
let cells=structuredClone(initial), drag=null, quiz=null;
const keys=["Ax","Ay","Bx","By"], m=Placement;
function render(){
  const t=copy[language];
  document.documentElement.lang=language;
  by("lang").textContent=language==="zh"?"English":"中文";
  for(const [id,i] of Object.entries({title:0,hint:1,reset:2,question:9,submit:10,reading:13,example:14}))by(id).textContent=t[i];
  const bad=keys.filter(k=>by(k).getAttribute("aria-invalid")==="true");
  by("feedback").textContent=bad.map(k=>k+" · "+t[8]+" [−2, "+(k[1]==="x"?10:8)+"]").join(" / ");
  by("quiz").textContent=quiz===null?"":t[quiz?11:12];
  const r=m.geometry(cells.A,cells.B);
  const legal=r.cells.every(v=>v.aligned&&v.inside)&&!r.overlap;
  by("result").textContent=t[3]+" "+r.area+" · "+t[4]+" A "+r.cells[0].row+", B "+r.cells[1].row+" · "+t[5]+" "+t[legal?6:7];
  for(const [id,c] of Object.entries(cells))by(id).setAttribute("transform","translate("+50*Number(c.x)+" "+(200-50*Number(c.y))+")");
}
for(const key of keys){
  const [id,k]=key, label=document.createElement("label"), input=document.createElement("input");
  label.textContent=id+"."+k+" "; input.id=key; input.inputMode="decimal"; input.value=cells[id][k];input.setAttribute("aria-invalid","false");
  label.append(input);by("inputs").append(label);
  input.oninput=()=>{
    try {cells[id][k]=m.coordinate(input.value,k);input.setAttribute("aria-invalid","false");}
    catch {input.setAttribute("aria-invalid","true");}
    render();
  };
}
function shift(id,k,origin,delta){
  if (Number(delta)===0)return;
  const next=m.move(origin,k,delta);
  cells[id][k]=next[k];const input=by(id+k);input.value=next[k];input.setAttribute("aria-invalid","false");
}
function point(e){
  return new DOMPoint(e.clientX,e.clientY).matrixTransform(by("board").getScreenCTM().inverse());
}
for(const id of ["A","B"]){
  const el=by(id);
  el.onkeydown=e=>{
    const action={ArrowRight:["x","0.1"],ArrowLeft:["x","-0.1"],ArrowUp:["y","0.1"],ArrowDown:["y","-0.1"]}[e.key];
    if(action){e.preventDefault();shift(id,action[0],cells[id],action[1]);render();}
  };
  el.onpointerdown=e=>{
    if(drag||e.button!==0)return;
    drag={id,ptr:e.pointerId,start:point(e),origin:{...cells[id]},axes:new Set()};
    el.setPointerCapture(e.pointerId);el.focus();
  };
  el.onpointermove=e=>{
    if(!drag||drag.id!==id||e.pointerId!==drag.ptr)return;
    const pos=point(e);
    for(const k of ["x","y"]){
      const delta=m.dragDelta((pos[k]-drag.start[k])/(k==="x"?50:-50));
      if(Number(delta)!==0)drag.axes.add(k);
      if(drag.axes.has(k)){
        const v=m.move(drag.origin,k,delta)[k];cells[id][k]=v;
        by(id+k).value=v;by(id+k).setAttribute("aria-invalid","false");
      }
    }
    render();
  };
  el.onlostpointercapture=el.onpointerup=el.onpointercancel=e=>{if(drag?.ptr===e.pointerId)drag=null;};
}
by("lang").onclick=()=>{language=language==="zh"?"en":"zh";render();};
by("form").onsubmit=e=>{e.preventDefault();try{quiz=m.cmp(by("answer").value,"0.5")===0;}catch{quiz=false;}render();};
by("answer").oninput=()=>{quiz=null;render();};
by("reset").onclick=()=>{
  drag=null;cells=structuredClone(initial);
  for(const k of keys){by(k).value=cells[k[0]][k[1]];by(k).setAttribute("aria-invalid","false");}
  by("answer").value="";quiz=null;render();
};
render();
