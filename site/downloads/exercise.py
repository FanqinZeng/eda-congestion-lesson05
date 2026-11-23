# Complete the two functions; each candidate path must count its bend once.
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
