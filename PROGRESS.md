# 制作进度

## 当前状态：已完成并公开验收

2026-11-24 04:09（Asia/Shanghai），在当天14:00截止之前完成。公开主页：https://fanqinzeng.github.io/eda-congestion-lesson05/ 。生产提交09038c05ae812ffac575b33f3a3251e6251847bf，GitHub Actions 45255758475 completed/success；仓库About主页入口已设置。

真实线上Edge完整学习路径18项通过，包括双语网页、编辑/拖动/键盘、练习、在线完整资料、影片播放/章节seek/语种字幕与倍速、真正CPython输出/异常/停止/live/超时。两个1080p30双语旁白版本均已完整解码；公开主页及15项资源HTTP200/206，HTML/JS/CSS/参考Python/示例/字幕/manifest逐字节散列与生产源一致，MP4支持206读取。真实BFCache返回保留代码并再次执行成功。

试点保留skill v1；根据真实网页、样片、完整成片和整课审阅迭代后冻结v2.0.0，详见docs/skill-iteration.md及docs/skill-history/。

报告：docs/qa/deployment.json、public-resources.json、navigation-online.json、media.json和独立审阅before/after。完整人工听审与物理触屏设备测试未做，未将自动验收写成这些人工验收。后续文档提交不改变已发布site内容。

## skill维护：v2.1.0

按用户后续要求将第二课验收经验写回skill，当前工作副本升级至v2.1.0，详情docs/skill-update-v2.1.md。原始消费v2.0.0及散列继续保留在历史快照；本次更新不改网页、影片或原有发布源。新版结构、历史证明回归、独立微型源码包与实际Edge试用均通过，五文件版本快照及散列已保存。

## 制作历史（以下记录保留当时状态）

2026-11-24，Asia/Shanghai。目标截止：今天14:00。

初始提交 f7d89ce 已实际推送，GitHub Pages已启用public=true、build_type=workflow。发布流水线随site变更触发，尚未上传课程网页，因此尚未有已交付的公开成品。

初始skill已建立并通过官方结构验证，拥塞仓库保留v1快照。中英文TTS实际短样音均可解码且非静音。上游固定003bcd49e3794e6cfd2680181cdbd347d673ad07，module与common共33个文本文件已保存于当前VLSI项目course-production-20261124/research/。

每30分钟制作任务已ACTIVE，id=skill，接续本聊天；目标14:00前交付。当前没有需用户处理的授权阻塞。

接续course-production-20261124/PLAN.md、PROGRESS.md和research/source-semantics.md。先用v1完成拥塞网页及真实成片，根据观察迭代skill，冻结后再一次制作合法化课程。现阶段不得把源预检或skill试用写成产品验收。

## 本轮实际完成

纯引擎、独立Python、完整双语网页/实验/练习/阅读页/真实Worker Python和两种完整旁白影片已经本地生成。片长303.67秒，14个语义场景，各1920×1080/30fps/H.264/AAC，含默认内嵌双语字幕和外部VTT、章节、封面、全文文字稿。影片全部解码和音量检查通过。

真实实帧与样片发现并修复中文换行丢字、数值越格、多pin身份、单步/合计混淆；真实手机浏览器发现并修复章节被隐藏。详细观察与可泛化修正规则见docs/skill-iteration.md；v1快照保留，中央skill v2候选待独立审阅后冻结。

Node引擎与播放器10项测试、独立Python交叉核对、字体回归、静态资源与真实Edge完整学习路径已通过；当前最终增加Stop/live及重新编码影片回归。真实人工完整听审和物理触屏未做。

独立整课审阅已完成，发现的5项重要问题及2项教学说明问题已修复；真实回归保存before/after。完整套件与实际媒体检查通过。v2.0.0五文件已冻结并保存散列，初始v1不变。

## 公开发布已验证

2026-11-24：课程已公开发布 https://fanqinzeng.github.io/eda-congestion-lesson05/ 。生产提交57ac3d365ccd19f61e06f30e366e504274f975b7，Actions运行45249418282 completed/success。

实际公开主页、reading、python、JS/CSS、双语VTT、两部MP4和WASM均HTTP200/206。真实线上Edge完整学习路径17项通过，包括项目子路径、双语片seek、真实CPython输出、异常、停止、live和超时恢复，详见docs/qa/deployment.json与public-resources.json。完整人工听审和物理触屏限制仍保留。

拥塞试点及真实产物驱动的skill迭代已完成。合法化正在一次消费冻结v2.0.0；其迁移五文件散列已验证，记录在第二仓库docs/skill-transfer.json。后续只修复有证据的实际问题。
