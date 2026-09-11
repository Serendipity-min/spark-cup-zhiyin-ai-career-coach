# 职引 · AI职业诊断官 —— API 批量自动化回归测试工程

本模块为「职引 · AI职业诊断官」星辰工作流的自动化 API 回归测试框架。支持针对发布后的 OpenAPI 工作流接口执行全流程多轮对话回归、状态机验证、岗位保真度校验、异常注入测试与六大章节质量断言。

## 一、目录结构

```text
api_regression/
├── README.md               # 本说明文档
├── requirements.txt        # Python 依赖清单
├── .env.example            # 环境变量配置模板（请勿提交真实 .env）
├── cases/
│   └── career_cases.yaml   # 全量测试用例集（标准用例/稳定性用例/状态机用例）
└── src/
    ├── xfyun_client.py     # 讯飞星辰 OpenAPI 客户端（支持 chat/completions 与 resume）
    ├── sse_parser.py       # SSE (Server-Sent Events) 流式协议解析器
    ├── runner.py           # 自动化测试执行引擎（支持单测/批量/会话重置/断点恢复）
    ├── assertions.py       # 质量断言引擎（章节完整性/六大维度/岗位保真/违禁词/占位符）
    └── report.py           # 测试报告生成器（自动汇总 Markdown/CSV/JSON）
```

## 二、环境依赖与安装

- **Python 版本**：Python 3.10+
- **安装依赖**：
  ```bash
  pip install -r requirements.txt
  ```

## 三、环境变量配置

复制 `.env.example` 为 `.env` 并填入讯飞星辰平台获取的 API 凭据：

```bash
cp .env.example .env
```

`.env` 字段说明：

```ini
# 讯飞星辰 OpenAPI 端点
XFYUN_API_URL=https://xingchen-api.xf-yun.com/workflow/v1/chat/completions
XFYUN_RESUME_URL=https://xingchen-api.xf-yun.com/workflow/v1/resume

# 工作流发布为 API 后的凭据
XFYUN_API_SECRET=your_api_secret_here
XFYUN_API_KEY=your_api_key_here
XFYUN_FLOW_ID=your_flow_id_here
```

## 四、测试执行方法

在 `api_regression/` 目录下运行：

```bash
# 运行全量测试用例（默认顺序执行 concurrency=1）
python -m src.runner

# 指定用例执行
python -m src.runner --case T01
python -m src.runner --case STATE_RESET
python -m src.runner --case ABORT_AND_SWITCH
```

测试完成后将在 `reports/` 目录下输出：
- `latest_report.md`：详细 Markdown 格式审计报告
- `summary.csv`：各用例指标与耗时统计表格
- `summary.json`：全量结构化执行结果数据
- `reports/raw/*.jsonl`：全生命周期原始交互与 SSE 响应轨迹（敏感凭据已脱敏）
