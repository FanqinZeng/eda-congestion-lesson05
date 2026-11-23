"""Independent reference: x-major GCell matrices, path occupancy or upstream leg toy.

Path mode is the authored correction to the transcript; it is not the upstream
helper. RUDY matched uses the same total mass per net for spatial comparison.
"""
import json,math,sys

def estimate(data, mode='path', capacity=None, positions=None):
    positions = data['placement'] if positions is None else positions
    capacity = data['capacity'] if capacity is None else capacity
    if not math.isfinite(capacity) or capacity <= 0: raise ValueError('capacity')
    if mode not in ('path','upstream'): raise ValueError('mode')
    grid=data['gcell']; nx,ny=grid['nx'],grid['ny'];cw,ch=grid['cellW'],grid['cellH']
    for p in positions.values():
        if not all(math.isfinite(p[k]) and 0<=p[k]<=data['chip'][bound] for k,bound in [('x','W'),('y','H')]):raise ValueError('coordinate')
    def tile(p):return min(nx-1,int(p['x']//cw)),min(ny-1,int(p['y']//ch))
    def grid0():return [[0.0 for _ in range(ny)] for _ in range(nx)]
    def walk(a,b):
        steps=max(abs(a[0]-b[0]),abs(a[1]-b[1]))
        if steps==0:return [a]
        dx=(b[0]-a[0])//steps;dy=(b[1]-a[1])//steps
        return [(a[0]+t*dx,a[1]+t*dy) for t in range(steps+1)]
    demand,raw,matched=grid0(),grid0(),grid0()
    for net in data['nets']:
        if len(net)<2 or len(set(net))!=len(net) or any(k not in positions for k in net):raise ValueError('pin')
        pins=[positions[k] for k in net];xmin=min(p['x'] for p in pins);xmax=max(p['x'] for p in pins);ymin=min(p['y'] for p in pins);ymax=max(p['y'] for p in pins)
        center={'x':(xmin+xmax)/2,'y':(ymin+ymax)/2}
        spokes=[(pins[0],pins[1],1)] if len(net)==2 else [(center,p,1/len(net)) for p in pins]
        mass=0
        for a,b,weight in spokes:
            start,end=tile(a),tile(b)
            for turn in [(end[0],start[1]),(start[0],end[1])]:
                legs=[walk(start,turn),walk(turn,end)]
                if mode=='path':
                    cells=set(legs[0]+legs[1]); contributions=[(cell,.5*weight) for cell in sorted(cells)]
                else:contributions=[(cell,.5*weight/len(leg)) for leg in legs for cell in leg]
                for (i,j),value in contributions:demand[i][j]+=value;mass+=value
        a,b=tile({'x':xmin,'y':ymin}),tile({'x':xmax,'y':ymax})
        box=[(i,j) for i in range(a[0],b[0]+1) for j in range(a[1],b[1]+1)]
        for i,j in box:raw[i][j]+=(xmax-xmin+ymax-ymin)/len(box);matched[i][j]+=mass/len(box)
    overflow=[max(0,v-capacity) for col in demand for v in col]
    return {'demand':demand,'rudyRaw':raw,'rudyMatched':matched,'metrics':{'total':sum(overflow),'max':max(overflow,default=0),'count':sum(v>1e-12 for v in overflow)}}

if __name__=='__main__':
    records=json.load(sys.stdin)
    print(json.dumps([estimate(item['data'],item.get('mode','path')) for item in records]))
