# 上游语义预检：后续制作必须明确

固定提交：003bcd49e3794e6cfd2680181cdbd347d673ad07。两课的module和common依赖均已下载。这里只是源语义预检，不是新课程算法测试或成片验收。

## 拥塞

讲稿提出两条L各半概率、不要重复计算转角；但common/solvers.py的实际`_deposit_line`每条leg把0.5均摊到该leg的GCell，四条leg合计2单位；零长leg仍向一个tile加量。多pin中心星形每spoke按1/p缩放。RUDY则把HPWL均匀分到bbox tiles。因此两个原始实现的总需求单位不同。

制作时必须明确这一区别：如果复现原helper就诚实标记“上游toy的每leg归一化约定”，解释其退化情形；如果按讲稿修正为每条完整路径去重，必须固定其GCell、角点、零长、multi-pin和归一化定义，注明与helper的差异并用独立Python验证。不能同时声称严格复现helper与不重复角点，却悄悄采用另一套算法。对RUDY和L需求的absolute overflow比较必须交代同一单位或明确不同比例，不能用未对齐的总量宣称一个模型更好。

使用audit-upstream.py生成的congestion-upstream-conventions.json核对已有源行为，但新产品仍需独立测试和自己的goldens。

## 合法化

独立skill试用实际核对了common/solvers.py与legalizationutil.py，报告和数值见skill-forward-test.md、legalization-conventions.json。

- Python round为ties-to-even，JS Math.round不同；半整数边界必须显式统一并测试。
- greedy snap后黄金例仍有重叠；不要讲成完整合法化。
- 总L1位移4.4包含所有cell，movable-only为3.8；指标口径必须明示。
- HPWL按cell center并包含width/height，黄金例32；不能照搬前课point-pin算法。

不要现在把这些预检当作“已经根据拥塞网页和成片完成skill迭代”。试点实际产物与观察仍是冻结迁移版的前置。
