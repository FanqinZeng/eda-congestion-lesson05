# 一张网，两种可能 · Congestion Lesson 05

关于概率L形布线需求的中英文交互课程，对应 [eda-learning issue #43](https://github.com/yongfu-li/eda-learning/issues/43) 与固定上游 [module02-03-probabilistic-demand](https://github.com/yongfu-li/eda-learning/tree/003bcd49e3794e6cfd2680181cdbd347d673ad07/courses/learn_congestion/module02-03-probabilistic-demand)。

公开入口：[课程主页](https://fanqinzeng.github.io/eda-congestion-lesson05/)。实际部署与验收状态以 [PROGRESS.md](PROGRESS.md) 的实际部署记录为准。

## 课程

- 全站中文 / English，语言切换保留实验；影片画面和旁白默认跟随界面语言。
- 可编辑坐标、拖动与键盘移动，实时重算L需求和RUDY；候选路径逐条审计、容量与精确格子指标。
- 默认模型按完整路径去重，另保留上游helper逐leg归一化兼容模式。逐net等总量比较与原始HPWL模式明确区分，详见在线讲义和 [设计裁决](docs/course-design.md)。
- 两个1080p / 30fps完整配音版本，各303.67秒，14个语义场景；中文和英文画面分别本地化。每片有真实AAC旁白、内嵌同屏双语字幕及WebVTT、章节、封面和全文文字稿。
- 真正Worker CPython / Pyodide交互台，可编辑执行、实时运行、异常、停止及5秒超时恢复；运行时按需从本地静态资源载入。
- 完整双语讲义、源码、练习、数据、文字稿可直接在线阅读与复制，下载为可选补充；六题带解释的自测与本机学习记录。

## 本地运行与验证

```bash
python3 scripts/serve.py --port 8185
node --test tests/*.test.mjs
python3 scripts/build-python.py
python3 scripts/build_reading.py --check
python3 scripts/check-site.py
```

媒体制作依赖见 requirements-media.txt，使用Python 3.12+的隔离环境。现有静态课程运行无需Python安装或CDN。

```bash
node scripts/export-data.mjs
python scripts/speech.py
python scripts/render-film.py --stills
python scripts/render-film.py
python scripts/render-film.py --lang en
python scripts/build_reading.py
python scripts/verify-media.py
python -m unittest discover -s tests -p 'test_*.py'
python scripts/check-browser.py --media
```

`video/story.json`有可编辑的双语语义单元，`video/data.json`由真实JS引擎导出。音频与来源按语义单元冻结，文字不变时不重新调用TTS。实际音频与两种字幕的阅读时间共同决定时间轴。`film_common.py`负责字体、时间轴、字幕和编码，`render-film.py`负责本课算法图形。

数值、实际浏览器与实际成片报告在 [docs/qa](docs/qa)；skill从初稿到真实产物驱动的迭代见 [docs/skill-iteration.md](docs/skill-iteration.md)。未做完整人工听审或真实触屏设备测试，不将自动验收等同于这些人工检查。

新代码MIT，新教材CC BY 4.0；第三方字体、Pyodide和来源见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
