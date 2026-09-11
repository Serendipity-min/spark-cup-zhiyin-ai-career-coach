# 职引 · AI职业诊断官 —— 平台导入与 API 自动化复现说明

本指南提供从零在科大讯飞星辰 Agent 平台导入工作流、绑定知识库与插件、发布 API 以及执行 Python 自动化回归测试的完整端到端复现指引。

---

## 一、星辰平台复现操作流程

### 步骤 1：登录平台并创建应用
1. 访问并登录 [科大讯飞星辰 Agent 平台](https://agent.xfyun.cn)；
2. 进入工作台，选择“创建智能体”或“创建工作流应用”。

### 步骤 2：导入工作流 DSL
1. 在工作流编辑界面点击右上角“导入工作流”；
2. 选择上传交付包中的 `workflow/职引_AI职业诊断官_Final.yml` 文件；
3. 平台将自动解析并恢复 **22 个节点与 28 条连线** 的拓扑结构。

### 步骤 3：创建知识库并上传文档
1. 在平台左侧导航栏进入“知识库管理”；
2. 新建知识库，命名为 `职引 · AI职业诊断官`；
3. 将 `knowledge_base/` 目录下的 **10 篇 Markdown 文档** 全部上传；
4. 解析设置：保持默认的分段与向量化索引，等待切片索引构建完成。

### 步骤 4：绑定插件与知识库资源
1. 返回工作流编辑器，定位到 `knowledge-base::a8726d32-5e7c-4f18-8cbc-05e942663ed6` 节点，选择并绑定刚才创建的知识库；
2. 定位到 `plugin::927eb11e-7629-4ad8-b557-d1915dbb155e` 节点，确保“联网搜索”插件授权处于激活状态；
3. 检查 `spark-llm` 节点的模型授权（确保开通 Spark Max 或相应模型权限）。

### 步骤 5：在线调试验证
在右侧调试面板中输入：
- 输入：“你好”
- 预期返回 Q1 提问：“你目前最想投递的目标岗位是什么？”
- 输入：“算法工程师”
- 预期返回 Q2 提问：“你的专业与年级是？”
- 输入：“计算机科学与技术，大三”
- 预期返回 Q3 提问：“你掌握哪些技能或有哪些项目实习经历？”
- 输入：“熟悉 Python、PyTorch、LeetCode 刷题 200 道，暂无大厂实习”
- 预期生成：包含六大章节与评分的完整职业诊断报告。

### 步骤 6：发布为 OpenAPI
1. 调试通过后，点击“发布工作流”；
2. 在“发布渠道”中勾选并启用“API 服务”；
3. 获取对应的 `flow_id`、`API Key` 与 `API Secret`。

---

## 二、本地 API 批量自动化回归测试

### 1. 安装 Python 运行依赖
进入 `api_regression/` 目录：
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
```
编辑 `.env` 填入真实凭据（注意：切勿将真实 `.env` 提交至公开仓库）：
```ini
XFYUN_API_URL=https://xingchen-api.xf-yun.com/workflow/v1/chat/completions
XFYUN_RESUME_URL=https://xingchen-api.xf-yun.com/workflow/v1/resume
XFYUN_API_KEY=your_actual_api_key
XFYUN_API_SECRET=your_actual_api_secret
XFYUN_FLOW_ID=your_actual_flow_id
```

### 3. 执行回归测试套件
```bash
# 执行全量回归套件 (concurrency=1)
python -m src.runner
```

### 4. 预期耗时与性能基准
- **多轮中断交互**：前 3 轮问答中断响应时间通常在 **1.5s ~ 3.5s** 以内；
- **最终报告生成**：因包含联网检索、知识库检索与长文本深度生成，平均耗时约为 **91.83 秒**；
- **异常兜底**：当联网搜索或知识库返回空结果时，工作流采用超时降级策略与常识兜底，不中断生成。
