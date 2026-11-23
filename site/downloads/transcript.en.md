# One Net, Two Routes



## 00:00:00.000 · Where could a wire create a bottleneck?



Two pins need a connection, but no wire has been routed yet. Can we predict which grid cells may carry more demand?

We will study a small model: two possible L-shaped routes, each with half the probability. Then we add their contributions cell by cell.



## 00:00:20.500 · Two possible bends, not two simultaneous wires



First, horizontal then vertical: follow A’s row to B’s column, then move up to B. This is one candidate route.

The other candidate goes vertical then horizontal. We do not know which one will be selected, so each candidate has probability one half.



## 00:00:39.567 · A bend is one visit



Look at the bend of the horizontal–vertical candidate. It belongs to both a horizontal leg and a vertical leg, but the complete route visits it once.

Deduplicate cells within the complete path before adding point five to each one. Turning a corner must not double the visit probability.



## 00:01:00.667 · Endpoints belong to both candidates



The endpoint cells containing A and B are different. Both candidates visit them, so each receives point five plus point five, giving one.

Boundary cells on just one candidate receive point five. Interior cells visited by neither receive zero. Every number has a route behind it.



## 00:01:21.867 · Turn routes into a demand matrix



In this four-by-four example, each candidate visits seven distinct cells. Seven times one half, plus seven times one half, gives total demand seven.

Our matrix is stored by column, and the diagram’s y-axis points upward. Array indices, screen direction and chip coordinates are different conventions.



## 00:01:43.900 · Capacity turns demand into overflow



Set each cell’s capacity to point six. The two endpoints have demand one, so each overflows by point four. Total overflow is point eight.

Demand equal to capacity means exactly full, with zero overflow. Lowering capacity leaves demand unchanged, but may create more hotspots.



## 00:02:06.000 · Same mass, different spatial distribution



RUDY spreads demand over the whole bounding box. To compare spatial distribution alone, we first match each net’s total mass to the L model.

Here, mass seven spread over sixteen cells gives point four three seven five per cell. No hotspot appears, but the route corridors have been smoothed away.



## 00:02:27.967 · Different units cannot directly rank models



Raw RUDY uses half-perimeter wirelength as its total mass. In this example that length is eighteen, a different unit from occupancy mass seven.

We retain raw values for reproduction and use matched mass to compare distributions. A smaller overflow number alone does not make a model better.



## 00:02:49.067 · Aligned pins make the candidates coincide



If both pins are on the same row, the candidates visit the same four cells. Each cell receives two half contributions, giving demand one.

Coincident routes do not mean discarding one candidate. We remove duplicate cells within a route, while contributions from distinct candidates still add.



## 00:03:10.667 · The same-cell case exposes the unit



When both pins occupy one cell, each candidate reduces to that cell. Our endpoint-inclusive occupancy model still assigns it one unit.

If the physical coordinates coincide, half-perimeter length can be zero. There is no contradiction: occupancy, wirelength and physical track counts are different quantities.



## 00:03:33.300 · Multi-pin nets use a center-star approximation



For a multi-pin net, find the bounding-box center and connect it to every pin. Each spoke still has two L-shaped candidates.

We retain the source convention of weight one over p per spoke. This is an explicit approximation, not a minimum Steiner tree or an obstacle-avoiding router.



## 00:03:55.167 · Reproduce the source without hiding its convention



The teacher’s helper spreads point five over each leg’s cells, giving total mass two across four legs. Those values are not per-cell visit probabilities.

The site offers a separate source-compatibility mode. The default complete-path deduplication follows the transcript’s meaning. The selected convention is always shown.



## 00:04:18.633 · A heat map is not a routed solution



This model omits metal layers, obstacles, shared trees, vias and detours under congestion. It offers quick placement feedback, not a completed route.

Compare models on the same input and compatible units, then validate with a more detailed router. Color alone is not a conclusion.



## 00:04:40.700 · Now change one number yourself



Open the lab, move a pin and inspect each candidate’s contribution. Predict a bend, an endpoint and a hotspot before checking your answers.

Then run the same data in the Python workspace. First define the routes and units, then compute demand, and only then trust the heat map.
