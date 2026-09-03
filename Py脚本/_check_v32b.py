# -*- coding: utf-8 -*-
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.2_字段提取修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('=== v3.2 QA 节点关键配置 ===\n')
for nid in ['question-answer::c17e1d8f', 'question-answer::8b7f2f5a', 'question-answer::3f928444']:
    n = next(x for x in d['flowData']['nodes'] if x['id'].startswith(nid))
    label = n['data']['nodeMeta']['aliasName']
    np = n['data']['nodeParam']

    print(f'【{label}】')
    da = np.get('directAnswer', {})
    print(f'  maxRetryCounts: {da.get("maxRetryCounts", "?")} ← 关键修复')
    print(f'  question 长度: {len(np.get("question", ""))} 字符')
    for o in n['data'].get('outputs', []):
        desc = o.get('schema', {}).get('description', '(无描述)')
        print(f'  字段 {o["name"]:15s}: {desc[:130]}')
    print()