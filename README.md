# 职引 · AI职业诊断官 (Zhiyin AI Career Coach)

> 🎯 **面向大学生的深度就业竞争力诊断智能体** —— 2026 科大讯飞“星火杯”大模型应用开发大赛复赛项目

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: iFlytek Xingchen](https://img.shields.io/badge/Platform-iFlytek%20Xingchen-blue)](https://agent.xfyun.cn)
[![DSL Version](https://img.shields.io/badge/DSL-v1-green.svg)]()
[![Workflow Nodes](https://img.shields.io/badge/Nodes-22-orange.svg)]()
[![Workflow Edges](https://img.shields.io/badge/Edges-28-blueviolet.svg)]()

---

## 一、项目简介

　　「职引 · AI职业诊断官」依托科大讯飞星辰 Agent 平台，创新性构建了 **22 个节点、28 条连线** 的高内聚状态机工作流。系统通过 3 轮结构化问答深度挖掘学生的求职目标、教育背景与核心技能实践，动态融合 **公开校招实时 JD 检索** 与 **10 篇专业 RAG 知识库资产**，由 Spark 大模型生成包含六大核心章节、量化打分（1.0~10.0）与 4 周冲刺行动计划的深度职业诊断报告，并通过 Python 轻量质量门禁保障输出合规性。

---

## 二、系统核心特性与事实基线

- **精准意图预识别**：零样本意图分类，支持求职目标提取、会话状态重置与多轮断点恢复。
- **状态机健壮性**：会话变量闭环控制，支持中途修改岗位（Abort & Switch）与重新开始（State Reset）。
- **多源证据融合**：严格遵循“用户自述 > 实时 JD > 专业知识库 > 模型常识”的优先级，杜绝凭空编造与幻觉。
- **六大维度量化评估**：根据目标岗位动态拆解 6 项核心能力维度，输出 S / A / B / C 四级准备度评级与证据覆盖度指标。
- **自动化 API 回归测试工程**：配套全套 Python 批量回归测试套件，提供自动化状态机验证与六大章节断言。

---

## 三、代码仓库与交付目录

```text
spark-cup-zhiyin-ai-career-coach/
├── README.md                      # 仓库主说明文档
├── DELIVERY_AUDIT.md              # 交付审计与安全检查报告
├── 04-项目代码/                    # 复赛官方最小可复现交付包
│   ├── README.md                  # 交付包详细说明
│   ├── workflow/
│   │   └── 职引_AI职业诊断官_Final.yml  # 22节点/28连线工作流 DSL
│   ├── knowledge_base/            # 10篇专业 RAG 知识库 Markdown 文档
│   │   ├── README_知识库清单.md
│   │   └── *.md
│   ├── api_regression/            # Python 自动化回归测试工程
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   ├── cases/career_cases.yaml
│   │   └── src/*.py
│   ├── docs/                      # 架构说明/参数表/复现指南
│   │   ├── 架构说明.md
│   │   ├── 工作流节点与参数表.md
│   │   └── API复现说明.md
│   └── SHA256SUMS.txt             # 交付文件完整性校验哈希表
├── 05-其他/                       # 测试与知识库全量审计证据包
│   ├── INDEX.md / INDEX.pdf       # 05-其他 导航索引与事实查验表
│   ├── README.md                  # 模块全景与归档说明
│   ├── 01_API自动化回归测试/       # 42例回归测试报告、量化指标、代表性原始流式日志
│   ├── 02_知识库资产/             # 10篇文档资产清单、平台截图与代表性文档
│   ├── 03_运行效果截图/           # 16:9工作流全景、节点执行、多轮问答、报告实测图
│   └── 04_版本迭代证据/           # 初赛vs复赛演进对比与关键缺陷修复审计
```

---

## 四、快速复现指南

1. **导入工作流**：在 [星辰平台](https://agent.xfyun.cn) 导入 `04-项目代码/workflow/职引_AI职业诊断官_Final.yml`；
2. **构建知识库**：新建知识库并上传 `04-项目代码/knowledge_base/` 下的 10 篇 Markdown 文档；
3. **绑定插件**：绑定工作流中的知识库节点与联网搜索插件；
4. **在线调试 / API 发布**：测试 3 轮问答并发布工作流为 API；
5. **API 回归测试**：
   ```bash
   cd 04-项目代码/api_regression
   pip install -r requirements.txt
   cp .env.example .env  # 填入真实凭据
   python -m src.runner  # 运行自动化测试套件
   ```

---

## 五、版权与开源协议

本项目代码与文档遵循 [MIT License](LICENSE)。
