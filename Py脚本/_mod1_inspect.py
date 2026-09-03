import yaml, os, re
from collections import OrderedDict

# 读 yml（保留中文和注释）
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'

with open(fn, 'r', encoding='utf-8') as f:
    raw = f.read()

d = yaml.safe_load(raw)

def get_node(d, target_id):
    return next((n for n in d['flowData']['nodes'] if n['id'] == target_id), None)

# ===== 节点 ID（已知） =====
NODE_REPORT = 'spark-llm::b6927f92-d655-4c5d-92ad-deff6af18ba9'  # 大模型：生成诊断报告
NODE_QA1 = 'question-answer::c17e1d8f-8e96-4c77-9f8e-83222d463c25'  # 询问目标岗位
NODE_QA2 = 'question-answer::8b7f2f5a-d6e6-4d90-a0b8-3bb1886efad6'  # 询问教育背景
NODE_QA3 = 'question-answer::3f928444-790d-4fd6-a5d6-471ccd3bc5d3'  # 询问实践经验
NODE_END = 'node-end::051340b1-7118-4842-9ae5-fae466e13054'  # 结束节点

for nid, alias in [(NODE_REPORT, '生成诊断报告'),
                   (NODE_QA1, '询问目标岗位'),
                   (NODE_QA2, '询问教育背景'),
                   (NODE_QA3, '询问实践经验'),
                   (NODE_END, '输出诊断报告')]:
    n = get_node(d, nid)
    print(f'\n=== {alias} ===')
    print('找到:', n is not None)
    if n:
        params = n['data']['nodeMeta'].get('nodeParams', {})
        print('Has systemPrompt:', 'systemPrompt' in params)
        print('Has userPrompt:', 'userPrompt' in params)
        print('Has answerContent:', 'answerContent' in params)
        print('keys:', list(params.keys())[:20])