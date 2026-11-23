from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent/'eda-placement-lesson3'
presets=json.loads((ROOT/'site/downloads/examples.json').read_text())
reference=(ROOT/'site/downloads/reference.py').read_text().split("if __name__=='__main__':")[0]
def example(name):
    return reference+'\ndata=json.loads('+repr(json.dumps(presets[name]))+')\nresult=estimate(data)\nfor row in reversed(range(data["gcell"]["ny"])):\n    print(" ".join(f"{column[row]:.3f}" for column in result["demand"]))\nprint("total:",round(sum(map(sum,result["demand"])),6))\nprint("overflow:",result["metrics"])\n'
exercise='''# Complete the two functions; each candidate path must count its bend once.
# 完成两个函数：每条候选路径的转角只计一次。
def path_cells(a, b, order="HV"):
    # a,b are integer GCell tuples. Include endpoints. / 包含端点。
    raise NotImplementedError("Implement the complete, deduplicated path")

def demand(a, b, nx=4, ny=4):
    result = [[0.0 for _ in range(ny)] for _ in range(nx)]
    # Add 0.5 for each cell on each candidate. / 每条候选每格加0.5。
    raise NotImplementedError("Accumulate both candidates")

d=demand((0,0),(3,3))
assert len(path_cells((0,0),(3,3))) == 7
assert d[3][0] == 0.5, "Do not count the bend twice"
assert d[0][0] == 1, "Both candidates visit the endpoint"
assert sum(map(sum,d)) == 7
assert sum(map(sum,demand((0,0),(0,0)))) == 1
print("5 checks passed / 5项检查通过")
'''
(ROOT/'site/downloads/exercise.py').write_text(exercise)
examples={'reference':example('diagonal'),'asymmetric':example('multi'),'exercise':exercise}
(ROOT/'site/python/examples.mjs').write_text('export const RUN_TIMEOUT_MS=5000, LIVE_DEBOUNCE_MS=700, MAX_OUTPUT_CHARS=40000;\nexport const EXAMPLES='+json.dumps(examples,ensure_ascii=False)+';\n')
replacements={
 'Placement Lesson 3':'Congestion Lesson 05','PLACEMENT · LESSON 03':'CONGESTION · LESSON 05','lesson3-':'congestion05-',
 '亲手修改三种线网模型，用真正的 Python 立即验证结果。':'逐格重算概率L路径，用真正的Python验证端点、转角与溢出。',
 'Edit three net models and verify the results with real Python.':'Recompute probabilistic L routes and verify endpoints, bends and overflow with real Python.',
 '黄金样例：BBox = 4，Clique = 16，Star = 8。坐标使用曼哈顿距离，Star 默认以第一个引脚为中心。':'对角黄金例：总需求7，两个端点各1，转角0.5；容量0.6时总溢出0.8。矩阵按列存储，打印时y向上。',
 'Golden example: BBox = 4, Clique = 16, Star = 8. All distances are Manhattan; Star uses the first pin as its hub by default.':'Diagonal golden: total demand 7, endpoint 1, bend 0.5; total overflow 0.8 at capacity 0.6. Matrices are x-major; printed rows increase upward.',
 '参考实现 · 黄金样例':'独立参考 · 对角两点','Reference · Golden pins':'Independent reference · Diagonal pair','非对称引脚':'三pin中心星形','Asymmetric pins':'Three-pin center star',
 '← ':'','约 12 MB':'约 12 MB'}
for name in ['workspace.mjs','index.html','workspace.css']:
    text=(BASE/'site/python'/name).read_text()
    for a,b in replacements.items():text=text.replace(a,b)
    (ROOT/'site/python'/name).write_text(text)
print('Built real CPython examples and localized workspace')
