# Independent whole-course review and one fix pass

Reviewed range: c461a89..9394db2, fresh independent reviewer, code plus actual Edge and actual full MP4 decoding/frame inspection. Model: gpt-6.2-astra / xhigh. No remote or repository mutations by reviewer.

Important findings reproduced by the author:

1. Raw HPWL RUDY used occupancy capacity to produce 16 meaningless hotspots and gold outlines, also in the film. Fixed by retaining raw values/mass while suppressing its hotspot count and capacity outlines. The two language films are re-encoded from the corrected renderer.
2. BFCache restored a page whose Worker was terminated on pagehide. Fixed by relaunching on persisted pageshow while preserving editor/results. The browser regression explicitly enables BFCache, verifies a persisted document and checks the first new execution after return. Playwright's default disabling of BFCache is not accepted as lifecycle coverage.
3. Coordinate and heatmap rerenders discarded keyboard focus. Fixed by retaining coordinate DOM nodes and restoring the selected SVG cell; validation covers Tab into the next coordinate and Enter on a cell, not just one arrow key.
4. English initialization called video.load() and downloaded the MP4 before interaction. Fixed by configuring the initial localized resources without active switching/load. A fresh-browser network regression checks that no MP4 is requested until user action.
5. Capacity step constraints rejected 0.4375, and a later valid value retained the old error. Fixed by accepting arbitrary finite positive capacity and clearing successful validation diagnostics.

Ruling: Regraded the guided same-cell action from minor to important: retaining helper mode gives 2 while the adjacent teaching claim promises 1. The guided action now selects the promised path/matched convention; free preset selection preserves preferences.

Ruling: Qualified the complexity statement rather than leaving an inaccurate whole-engine claim: path deposition is visit-proportional, but this implementation also enumerates bounding boxes and copies full matrices per candidate. The notes now state those additional costs.

No second review is requested; before/after browser regressions and the complete suite verify the fix pass. Full human listening and physical touchscreen tests remain unperformed; this report does not claim public deployment or legalization transfer.
