from pathlib import Path
import json,math,argparse
from PIL import ImageDraw
from film_common import *
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--lang',choices=['zh','en'],default='zh');p.add_argument('--stills',action='store_true');p.add_argument('--sample',action='store_true');p.add_argument('--encode-only',action='store_true');a=p.parse_args()
film=Film(ROOT,a.lang);DATA=json.loads((ROOT/'video/data.json').read_text());R=DATA['results'];LANG=a.lang
def tr(zh,en):return zh if LANG=='zh' else en
def partial_line(draw,points,progress,color,width=4):
    lengths=[abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(points,points[1:])];left=sum(lengths)*max(0,min(1,progress))
    for a,b,length in zip(points,points[1:],lengths):
        f=min(1,left/length) if length else 1
        if left>=0:draw.line((a,(mix(a[0],b[0],f),mix(a[1],b[1],f))),fill=color,width=width)
        left-=length
def grid(im,matrix,x=130,y=300,u=111,routes=None,progress=1,cap=.6,highlight=(),pins=True,pin_points=None,values=True):
    d=ImageDraw.Draw(im);nx=len(matrix);ny=len(matrix[0]);xy=lambda p:(x+(p[0]+.5)*u,y+(ny-.5-p[1])*u)
    for i in range(nx):
        film.text(im,i,x+(i+.5)*u-8,y-32,21,MUTED,True)
        for j in range(ny):
            q=min(1,matrix[i][j]);fill=(round(12+q*55),round(40+q*100),round(49+q*73));rect=(x+i*u,y+(ny-1-j)*u,x+(i+1)*u-6,y+(ny-j)*u-6);color=GOLD if matrix[i][j]>cap+1e-9 else FAINT
            d.rounded_rectangle(rect,radius=5,fill=fill,outline=IVORY if (i,j) in highlight else color,width=3 if (i,j) in highlight or color==GOLD else 1)
    for j in range(ny):film.text(im,j,x-30,y+(ny-1-j)*u+38,21,MUTED,True)
    for r in routes or []:
        points=[xy(r['a']),xy(r['bend']),xy(r['b'])];color=GOLD if r['order']=='HV' else TEAL;partial_line(d,points,progress,color,5)
        # A route tracer keeps motion tied to the candidate path, not to a camera pan.
        if progress>=.999:
            lengths=[abs(b[0]-a[0])+abs(b[1]-a[1]) for a,b in zip(points,points[1:])];left=sum(lengths)*((CURRENT_TIME/7+(0 if r['order']=='HV' else .5))%1)
            for p,q,length in zip(points,points[1:],lengths):
                if left<=length:
                    f=left/length if length else 0;cx,cy=mix(p[0],q[0],f),mix(p[1],q[1],f);d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=color);break
                left-=length
    if values:
        for i in range(nx):
            for j in range(ny):
                value=matrix[i][j];label=('≈' if abs(value-round(value,4))>1e-8 else '')+n(value);size=film.fit_size(label,u-16,28,True);width=film.font(size,True).getlength(label)
                film.text(im,label,x+i*u+(u-6-width)/2,y+(ny-1-j)*u+u-42,size,IVORY,True)
    if pins and routes:
        labels=pin_points if pin_points is not None else [('A',routes[0]['a']),('B',routes[-1]['b'])]
        for k,(label,point) in enumerate(labels):
            cx,cy=xy(point);cy-=12;cx+=14 if k and point==labels[0][1] else 0;d.ellipse((cx-13,cy-13,cx+13,cy+13),fill=BG,outline=IVORY,width=2);film.text(im,label,cx-8,cy-15,23,IVORY,True)
    return xy
KEYS={
 'hook':('先明确候选路线，再预测需求。','Define the candidate routes before estimating demand.'),
 'paths':('P(HV) = ½    P(VH) = ½','P(HV) = ½    P(VH) = ½'),
 'corner':('同一条完整路径中，转角只计一次。','One complete candidate visits its bend once.'),
 'endpoint':('两个候选共享端点：½ + ½ = 1。','Shared endpoints: ½ + ½ = 1.'),
 'matrix':('7 × ½ + 7 × ½ = 7','7 × ½ + 7 × ½ = 7'),
 'capacity':('overflow(g) = max(0, D(g) − C)','overflow(g) = max(0, D(g) − C)'),
 'rudy':('等总量比较空间分布，不是给模型排名。','Match total mass to compare spatial distributions.'),
 'units':('占用、线长和物理轨数，是不同的单位。','Occupancy, wirelength and physical tracks have different units.'),
 'straight':('候选可以重合，概率仍然相加。','Candidates can coincide; their probabilities still add.'),
 'same':('本课包含端点，因此同格占用为 1。','Endpoints are included, so same-cell occupancy is 1.'),
 'multi':('中心星形是近似；每条辐条的权重为 1/p。','The center star is an approximation; each spoke has weight 1/p.'),
 'source':('默认讲稿修正与原helper兼容，明确分开。','The transcript correction and source compatibility stay distinct.'),
 'limits':('快速反馈 ≠ 实际布线解','A quick estimate is not a routed solution.'),
 'close':('定义 → 计算 → 验证','Define → Compute → Verify')}
assert abs(R['diagonal']['path']['totalDemand']-7)<1e-9
assert abs(R['diagonal']['path']['metrics']['total']-.8)<1e-9
assert abs(R['multi']['path']['totalDemand']-4)<1e-9
def frame(t):
    global CURRENT_TIME
    CURRENT_TIME=t
    im,s=film.frame_shell(t);d=ImageDraw.Draw(im);local=t-s['start'];phase=local/s['duration'];kind=s['kind'];gold=R['diagonal']['path'];matrix=gold['demand'];routes=gold['trace'];progress=ease(local/5)
    if kind in ['rudy','units','source']:
        right=gold['rudyMatched'] if kind=='rudy' else gold['rudyRaw'] if kind=='units' else R['diagonal']['upstream']['demand'];left=matrix
        film.text(im,tr('L 路径占用','L-route occupancy'),125,260,32,TEAL);film.text(im,tr('等总量 RUDY','Matched-mass RUDY') if kind=='rudy' else tr('原始 HPWL 单位','Raw HPWL units') if kind=='units' else tr('上游按腿归一化','Upstream leg normalization'),1035,260,32,GOLD)
        grid(im,left,x=130,y=322,u=104,routes=routes,progress=progress);grid(im,right,x=1040,y=322,u=104,routes=None,pins=False)
        film.text(im,'Σ D = 7',140,760,35,TEAL,True);film.text(im,'Σ D = '+n(sum(map(sum,right))),1050,760,35,GOLD,True)
        film.text(im,'7 / 16' if kind=='rudy' else '7 ≠ 18' if kind=='units' else '7 ≠ 2',650,455,62,IVORY,True)
        film.paragraph(im,tr('相同总量','Same mass') if kind=='rudy' else tr('不同单位','Different units'),665,560,290,29,MUTED)
    elif kind in ['straight','same','multi']:
        name={'straight':'straight','same':'same','multi':'multi'}[kind];r=R[name]['path'];matrix=r['demand'];routes=r['trace'];labels=None
        if kind=='multi':
            preset=DATA['presets']['multi'];g=preset['gcell'];labels=[(key,[int(p['x']//g['cellW']),int(p['y']//g['cellH'])]) for key,p in preset['placement'].items()]+[('O',routes[0]['a'])]
        grid(im,matrix,routes=routes,progress=progress,pin_points=labels)
        if kind=='straight':items=[('4',tr('个共同经过的格子','cells visited by both candidates')),('1',tr('每格期望占用','expected occupancy per cell'))]
        elif kind=='same':items=[('1',tr('期望占用总量','total expected occupancy')),('0',tr('原始半周长','raw half-perimeter wirelength'))]
        else:items=[('p = 3',tr('包围盒中心星形','bounding-box center star')),('1 / 3',tr('每条辐条权重','weight per spoke')),('Σ D = 4',tr('独立引擎计算','computed by the shared engine'))]
        for i,(value,label) in enumerate(items):film.text(im,value,870,315+i*145,63,TEAL if i%2==0 else GOLD,True);film.text(im,label,870,390+i*145,31,MUTED)
    else:
        highlight=[]
        if kind=='hook':matrix=[[0 for _ in c] for c in matrix];routes=routes[:1] if phase<.5 else routes[1:]
        if kind=='paths':routes=routes[:1] if phase<.5 else routes[1:];matrix=[[0 for _ in c] for c in matrix];progress=ease((local if phase<.5 else local-s['duration']*.5)/5)
        if kind=='corner':highlight=[(3,0)];routes=routes[:1];matrix=routes[0]['cumulative']
        if kind=='endpoint':highlight=[(0,0),(3,3)]
        if kind=='matrix':
            count=min(2,1+int(local>6));matrix=gold['trace'][count-1]['cumulative'];routes=routes[:count];progress=ease((local if count==1 else local-6)/4)
        cap=.6
        if kind=='capacity':cap=mix(1.1,.6,ease(local/2)) if phase<.5 else mix(.6,.4,ease((local-s['duration']*.5)/5))
        grid(im,matrix,routes=routes,progress=progress,cap=cap,highlight=highlight,values=kind not in ['hook','paths'])
        if kind=='hook':film.text(im,'A       B',880,345,90,IVORY,True);film.paragraph(im,tr('还没有一条确定的线，\n却已经可以提出可验证的预测。','No wire has been chosen yet. We can still make a checkable prediction.'),880,490,790,36)
        elif kind=='paths':film.text(im,'½',900,335,155,GOLD if phase<.5 else TEAL);film.text(im,'H → V' if phase<.5 else 'V → H',900,535,58,IVORY,True)
        elif kind=='corner':film.text(im,'0.5',880,330,130,GOLD,True);film.paragraph(im,tr('一个候选，只访问一次。\n先合并横腿和竖腿中的重复格子。','One candidate, one visit. Deduplicate the complete path before depositing demand.'),880,525,790,36)
        elif kind=='endpoint':film.text(im,'0.5 + 0.5',850,350,80,TEAL,True);film.text(im,'= 1',880,485,125,IVORY,True)
        elif kind=='matrix':film.text(im,'Σ D = '+n(sum(map(sum,matrix))),830,360,80,TEAL,True);film.paragraph(im,tr('每个格子都有一份可核对的贡献。\n数组按列存储，y 轴向上。','Every value has an auditable contribution. Matrices are x-major; y points upward.'),840,520,820,35)
        elif kind=='capacity':
            values=[max(0,v-cap) for c in matrix for v in c];film.text(im,'C = '+n(cap),860,315,70,GOLD,True);film.text(im,tr('热点 ','Hot cells ')+str(sum(v>1e-9 for v in values)),860,445,53,IVORY);film.text(im,tr('总溢出 ','Overflow ')+n(sum(values)),860,560,53,TEAL)
        elif kind=='limits':
            for i,j in [(3,1),(0,2)]:
                x=130+i*111;y=300+(3-j)*111;d.rectangle((x+3,y+3,x+103,y+103),outline='#d58e7e',width=4)
                for delta in range(10,90,20):d.line((x+delta,y+8,x+8,y+delta),fill='#d58e7e',width=2)
            film.paragraph(im,tr('障碍、层、过孔、共享树：\n此 toy 模型没有处理。','Obstacles, layers, vias, shared trees: not represented in this toy model.'),840,340,850,45);film.text(im,tr('示意障碍：路径并未绕开','Illustrative obstacles: paths do not detour'),840,650,28,'#d58e7e')
        elif kind=='close':
            for i,(value,label) in enumerate([('0.5',tr('转角','Bend')),('7',tr('总需求','Total demand')),('0.8',tr('容量0.6的总溢出','Overflow at capacity 0.6'))]):film.text(im,value,860,305+i*140,68,TEAL if i%2 else GOLD,True);film.text(im,label,1160,330+i*140,33,IVORY)
    film.text(im,KEYS[kind][0 if LANG=='zh' else 1],100,814,28,MUTED)
    return im
if not a.encode_only:film.output_materials(frame)
print(f'Timeline: {film.duration:.2f}s / {len(film.scenes)} scenes',flush=True)
if a.stills:film.stills(frame)
else:film.encode(frame,sample=a.sample)
