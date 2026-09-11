# 职引 · AI职业诊断官 —— 05-其他材料全景导航 (INDEX)

> 本文档为评审专家提供快速审阅导航，用可量化、可审计的工程化证据证明「职引」系统的高度稳定与可复现性。

---

## 第一屏：42/42 API 自动化测试核心指标摘要

<div class="metric-grid">
  <div class="metric-box">
    <div class="metric-title">全量案例有效通过</div>
    <div class="metric-val">42 / 42 <span class="badge-pass">100%</span></div>
  </div>
  <div class="metric-box">
    <div class="metric-title">六大章节完整覆盖</div>
    <div class="metric-val">252 / 252 <span class="badge-pass">100%</span></div>
  </div>
  <div class="metric-box">
    <div class="metric-title">岗位保真通过率</div>
    <div class="metric-val">42 / 42 <span class="badge-pass">100%</span></div>
  </div>
  <div class="metric-box">
    <div class="metric-title">模板变量泄漏</div>
    <div class="metric-val">0 例 <span class="badge-pass">零残留</span></div>
  </div>
  <div class="metric-box">
    <div class="metric-title">P50 / P95 响应耗时</div>
    <div class="metric-val">100.3s / 115.9s</div>
  </div>
  <div class="metric-box">
    <div class="metric-title">平均最终生成耗时</div>
    <div class="metric-val">91.83 s</div>
  </div>
</div>

- **测试执行方式**：零修改讯飞线上 Workflow，通过星辰 OpenAPI 全流程自动化调用。
- **详见报告**：[`01_API自动化回归测试/API回归测试报告.pdf`](01_API自动化回归测试/API回归测试报告.pdf) 与 [`latest_report.md`](01_API自动化回归测试/latest_report.md)。

---

## 第二屏：10 篇专业 RAG 知识库资产全景

知识库资产覆盖互联网 8 大核心岗位与非互联网重点行业（金融银行、国企、医疗、教师、制造业），由工作流节点 17 动态检索：
- **岗位事实类**：`职引_校招JD库.md`、`职引_JD库_非互联网行业.md`
- **学习路线类**：`职引_学习路线库.md`、`职引_学习路线库_全行业版.md`
- **面试准备类**：`职引_面试题库.md`、`职引_面试题库_全行业版.md`
- **简历投递类**：`职引_简历模板库.md`、`职引_投递策略库.md`、`职引_评分标准库.md`
- **真实案例类**：`职引_真实案例库.md`（9 大 985/211/双非求职复盘）
- **详见清单**：[`02_知识库资产/知识库资产清单.pdf`](02_知识库资产/知识库资产清单.pdf) 与代表性文档。

---

## 第三屏：状态机与关键场景专项验证

- **STATE_RESET（会话重置验证）**：Phase 1 生成完整报告后，在**同一会话 (fixed_uid + fixed_chat_id)** 下发送“你好”，首个中断严格重置为 Q1，无历史残留。
- **ABORT_AND_SWITCH（中途放弃并换岗）**：在 Q2 阶段发送 abort 指令（捕获 code=23802），同会话切换产品经理，最终报告 100% 切换且算法残留为 0.0%。
- **T02（首句跳过 Q1）**：首句直接输入岗位，严格断言仅触发 2 轮中断；
- **T08（信息补问）**：学历缺失时，严格断言触发 4 轮中断补全。
- **原始轨迹**：[`01_API自动化回归测试/representative_raw/`](01_API自动化回归测试/representative_raw/)。

---

## 第四屏：版本迭代与运行效果留痕

- **初赛 vs 复赛对比**：从 6 节点单链原型跨越至 22 节点状态机智能体，详见 [`04_版本迭代证据/初赛_vs_复赛对比.pdf`](04_版本迭代证据/初赛_vs_复赛对比.pdf)。
- **运行截图留痕**：[`03_运行效果截图/`](03_运行效果截图/) 提供 16:9 画布全景、Web/RAG 成功节点、多轮交互与六章报告高清图证。
