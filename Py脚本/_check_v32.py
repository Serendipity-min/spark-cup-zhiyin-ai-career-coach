# -*- coding: utf-8 -*-
import yaml, sys, json
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.2_字段提取修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('=== v3.2 QA 节点关键配置验证 ===\n')
for nid in ['question-answer::c17e1d8f', 'question-answer::8b7f2f5a', 'question-answer::3f928444']:
    n = next(x for x in d['flowData']['nodes'] if x['id'] == nid)
    label = n['data']['nodeMeta']['aliasName']
    np = n['data']['nodeParam']

    print(f'【{label}】')
    print(f'  maxRetryCounts: {np.get("directAnswer", {}).get("maxRetryCounts", "?")}')
    print(f'  answerType: {np.get("answerType", "?")}')
    print(f'  question 长度: {len(np.get("question", ""))} 字符')

    outputs = n['data'].get('outputs', [])
    print('  字段提取:')
    for o in outputs:
        desc = o.get('schema', {}).get('description', '(无)')
        print(f'    {o["name"]:15s}: {desc[:120]}')
    print()