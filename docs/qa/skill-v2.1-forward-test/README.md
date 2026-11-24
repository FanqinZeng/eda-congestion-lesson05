# Mini Placement

Open index.html locally. Add ?lang=en for English. Python 3.9+ standard library runs python3 generate.py to rebuild the bundled example and readable reference. Node.js 18+ runs node check.cjs. Run python3 verify.py after generation for JS/Python agreement and reproducibility. Browser interaction checks use Python Playwright and a Chromium browser. Set EDGE_PATH to an installed Edge executable and run python3 browser_check.py.

Cells use lower-left coordinates. Legal placement requires both cells to fit inside the chip, align to rows and sites within 1e-9 (layout units), and intersect with zero area. The nearest-row tie selects the lower row. Coordinates retain decimal precision. Bounds for editing and motion include a two-unit margin. Movement clamps at that margin. Drag deltas round to the nearest tenth, with ties away from zero. Invalid drafts stay visible while geometry uses the most recent valid coordinate. Reset restores both cells and the quiz.

Skill consumed: eda-lesson-studio v2.1.0. This is a bounded interaction and offline generation exercise.
