"""Copy only audited reusable assets; keep the prior course read-only."""
from pathlib import Path
import shutil,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent/'eda-placement-lesson3';AUDIT=ROOT.parent/'course-production-20261124/research'
for p in ['site/media','site/reading','site/python','video/fonts','video/audio','docs/qa','site/vendor','site/downloads']:(ROOT/p).mkdir(parents=True,exist_ok=True)
for name in ['NotoSansSC-Regular.otf','JetBrainsMono-Regular.ttf','OFL-noto-sans-sc.txt','OFL-jetbrains-mono.txt']:
 src=BASE/'video/fonts'/name
 if src.exists():shutil.copy2(src,ROOT/'video/fonts'/name)
shutil.copytree(BASE/'site/vendor/pyodide',ROOT/'site/vendor/pyodide',dirs_exist_ok=True)
shutil.copy2(BASE/'site/assets/player.mjs',ROOT/'site/assets/player.mjs')
shutil.copy2(BASE/'site/python/worker.mjs',ROOT/'site/python/worker.mjs')
shutil.copy2(BASE/'scripts/serve.py',ROOT/'scripts/serve.py')
shutil.copy2(BASE/'requirements-media.txt',ROOT/'requirements-media.txt')
shutil.copy2(BASE/'LICENSE',ROOT/'LICENSE')
shutil.copy2(BASE/'LICENSE-CONTENT.md',ROOT/'LICENSE-CONTENT.md')
data=json.loads((AUDIT/'upstream/courses/learn_congestion/common/tiny_cong.json').read_text())
(ROOT/'site/assets/teacher.mjs').write_text('export default '+json.dumps(data,ensure_ascii=False)+';\n')
print('Prepared licensed fonts, local Pyodide, generic player, Worker, and pinned teacher fixture')
