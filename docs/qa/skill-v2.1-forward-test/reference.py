"""Exact rational reference. Place two lower-left 1 by 2 cells."""
from fractions import Fraction as Q


def geometry(a, b):
    def box(p):
        x, y = map(Q, p)
        return ((x, x + 1), (y, y + 2))

    def shared(i, j):
        return max(Q(0), min(i[1], j[1]) - max(i[0], j[0]))

    ax, ay = box(a)
    bx, by = box(b)
    area = shared(ax, bx) * shared(ay, by)
    cells = []
    for pos in (a, b):
        x, y = map(Q, pos)
        row = min((0, 2, 4), key=lambda r: abs(y - r))
        aligned = max(abs(x - round(x)), abs(y - row)) <= Q("1e-9")
        cells.append(dict(row=str(row), aligned=aligned, inside=0 <= x <= 7 and 0 <= y <= 4))
    return area, cells


if __name__ == "__main__":
    for x in ("2", "1.9999999995", "2.0000000005"):
        area, _ = geometry(("1", "0"), (x, "0"))
        print(x, area, area > 0)
