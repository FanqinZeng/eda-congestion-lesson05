from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
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
# The committed workspace HTML/controller/CSS are authoritative lesson-local inputs.
# Regenerate only exercise/examples; preserve the tested BFCache lifecycle controller.
print('Built real CPython examples from local lesson sources')
