# -*- coding: utf-8 -*-
"""最终确认：展示 v3.1 的关键内容"""
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.1_修复版.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 展示 5 个关键修改
nodes = {
    'spark-llm::b6927f92': '大模型（systemTemplate）',
    'node-end::051340b1': '结束节点（template）',
    'node-end::051340b1': '结束节点（reasoningTemplate）',
    'question-answer::c17e1d8f': '问答1（question）',
    'question-answer::8b7f2f5a': '问答2（question）',
    'question-answer::3f928444': '问答3（question）',
}

for nid, label in nodes.items():
    for n in d['flowData']['nodes']:
        if n['id'].startswith(nid):
            np = n['data']['nodeParam']
            print(f'\n{"="*60}')
            print(f'【{label}】')
            print(f'{"="*60}')
            if 'systemTemplate' in np:
                s = np['systemTemplate']
                print(s[:800])
                print('...')
            elif 'question' in np:
                print(np['question'])
            elif 'template' in np and 'systemTemplate' not in np:
                print(np['template'])
            if 'reasoningTemplate' in np:
                print()
                print('[reasoningTemplate]:')
                print(np['reasoningTemplate'])
            break