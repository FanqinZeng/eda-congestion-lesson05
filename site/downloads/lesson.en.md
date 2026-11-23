# Probabilistic Demand: One Net, Two Possible Routes

## Goals and problem boundary

Inputs are chip dimensions, a GCell grid, pin positions, nets and capacity. Outputs are per-cell demand, congestion ratios and overflow. This is an early estimate before routing, not an optimizer or a manufacturable metal layout.

You will trace both L candidates, distinguish bends from endpoints, calculate a matrix, compare matched-mass RUDY distributions and identify missing physical factors. Basic coordinates and probability are sufficient.

## Terms and units

A GCell is a coarse chip region, a pin is a connection terminal, and a net groups pins requiring connection. Diagram segments join GCell centers to show visited cells; they are not exact physical wires.

Demand D is endpoint-inclusive expected GCell occupancy in this lesson. Capacity C must use that same toy unit. Congestion is D/C, oversubscription means D>C, and overflow is max(0,D-C). Equality means exactly full, with zero overflow.

## Deduplicate a complete path before depositing probability

A two-pin net has two candidates: horizontal–vertical and vertical–horizontal, each with probability 1/2. Concatenate a candidate’s two legs, remove repeated cells, and add 0.5 to each remaining cell. A bend belongs to both legs but is visited once by that complete candidate.

Contributions from distinct candidates still add. Shared endpoints receive 0.5+0.5=1; cells on one candidate receive 0.5; cells on neither receive zero. Linearity of expectation lets us sum net contributions without requiring independent nets merely to compute that expectation.

```text
for each net:
    for each star edge (a,b,weight):
        for order in [HV,VH]:
            cells = unique(complete_L_path(a,b,order))
            for g in cells:
                D[g] += 0.5 * weight
```

## Golden example: verify the total seven

The chip is 12×12, with a 4×4 grid of 3×3 cells. Pins A=(1,1) and B=(10,10) map to cells (0,0) and (3,3). The origin is at the bottom left and y increases upward. Each candidate visits seven distinct cells, giving mass 7×0.5+7×0.5=7.

```text
y=3    0.5  0.5  0.5  1.0
y=2    0.5  0.0  0.0  0.5
y=1    0.5  0.0  0.0  0.5
y=0    1.0  0.5  0.5  0.5
       x=0  x=1  x=2  x=3
```

Code stores matrix[x][y]. Printing reverses y, so do not confuse the outer array with top-to-bottom screen rows. At internal grid boundaries, floor selects the cell on the right or above. Positions exactly at the chip’s maximum boundary are clamped to the final cell.

## Treat capacity as a controlled variable

At capacity 0.6, only the two endpoints with demand 1 are oversubscribed. Each contributes overflow 0.4, giving total 0.8 and hotspot count two. Other boundary cells have demand 0.5 and are not oversubscribed. Lowering capacity to 0.4 changes the hotspot set without changing demand.

Change one factor at a time: keep coordinates fixed while changing capacity, then restore capacity before moving a pin. Inspect a cell’s exact D, C, D/C and overflow. Both maps share a color scale; gold outlines denote strict oversubscription, while a white outline denotes selection.

## Match units before comparing RUDY

Raw toy RUDY distributes a net’s half-perimeter wirelength over its bounding-box cells. This example has HPWL 18 across 16 cells, giving 1.125 per cell. Length-derived mass 18 cannot directly rank against occupancy-derived mass seven through absolute overflow.

By default, we match each net’s RUDY mass to its L-model mass before comparing spatial distributions. The example gives 7/16=0.4375 per cell. At capacity 0.6 RUDY has no hotspot while the L estimate has two. Neither result proves superior accuracy without a real routed reference. It does show that RUDY fills the box while the L model concentrates demand in candidate corridors.

Coincident physical positions can have HPWL zero but occupancy one. Matching distributes the L model’s mass over that net’s box directly, so it never divides by zero; raw RUDY retains zero. This is a useful counterexample about units.

## Multi-pin center-star approximation

For p pins, find the physical bounding-box center and connect it to every pin. Each spoke uses the same two-L construction with weight 1/p, retaining the upstream scaling convention. The center is virtual and need not be a pin.

The three-pin preset uses A=(1,1), B=(10,1), C=(10,10). Center (5.5,5.5) lies in GCell (1,1). Its spokes visit three, four and five cells per candidate, giving total mass (3+4+5)/3=4. This is not a minimum Steiner tree; it does not merge shared branches or guarantee obstacle avoidance.

## Aligned and same-cell cases

For aligned pins, both candidates visit the same four cells. Every cell receives two half contributions, giving demand one and total four. Removing a coincident candidate would incorrectly reduce the total probability to one half.

In the same-cell preset, each deduplicated candidate contains one cell and total occupancy remains one. Endpoint-inclusive occupancy is not wirelength. A physical router may use edge capacities or different terminal conventions; toy values are not track counts.

## Difference from the pinned source helper

The transcript describes half-probability L candidates and avoiding duplicate bends. However, the pinned common/solvers.py spreads 0.5 over each leg separately. Four legs have total mass two; zero-length legs still deposit mass and bends receive both legs’ shares. Its 1/p multi-pin scaling is retained here.

An explicitly labeled compatibility mode reproduces the helper. The default complete-path deduplication is an authored teaching correction. In the diagonal helper case, corners have 0.25, other boundary cells 0.125 and total mass two. Those numbers are not per-cell visit probabilities. Audit records and source comparisons are in docs/research; never mix answers from different conventions.

## Run real Python

The workspace runs CPython inside a separate Worker, loading bundled Pyodide on demand. Edit all the code, run it immediately or use live mode, inspect output and exceptions, and stop a run. Each execution has fresh variables. Stop or the five-second timeout restarts the interpreter while keeping code and existing output.

The reference independently implements the same conventions. The exercise asks you to complete path deduplication and demand accumulation, with five hand-checkable assertions. Printing a constant is not evidence of a working algorithm: also test aligned pins, same-cell pins, boundaries and three-pin stars. Code executes in this browser, not on a server.

## Complexity and limits

L-path deposition costs time proportional to the candidate-cell visits. This teaching implementation additionally enumerates each net’s bounding-box tiles for RUDY and copies the full nx×ny matrix per candidate to retain a trace. Total time therefore also includes those box visits and candidate-count times grid size; trace storage has that same extra factor. The demand matrix alone uses nx×ny space. This is not a memory-optimized large-chip design.

There are no metal layers, vias, obstacles, shared trees, timing objectives or congestion detours. Equal candidate probability is an assumption, not an empirical routing distribution. Use the model for early placement feedback and validate with a more detailed router. A heat map is not proof of completed routing.

## Continue experimenting

Predict bend 0.5, total seven and overflow 0.8 before checking your answers. Move a pin, align the pins, lower capacity and inspect raw RUDY units, explaining one cause each time. Finally load the teacher’s 4×2 six-net fixture and compare the corrected default with source compatibility, recording convention and capacity.

## Provenance

The lesson is based on Yongfu Li’s eda-learning, commit 003bcd49e3794e6cfd2680181cdbd347d673ad07, module02-03-probabilistic-demand and issue #43. Path deduplication, matched-mass comparison, the interactive site and new animation are authored by FanqinZeng. Credits and component licenses are on the home page and THIRD_PARTY_NOTICES.md. New code is MIT; new teaching content is CC BY 4.0; third-party components retain their licenses.
