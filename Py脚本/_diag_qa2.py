# -*- coding: utf-8 -*-
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.1_FINAL.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('所有 QA 节点 ID：')
for n in d['flowData']['nodes']:
    if 'question-answer' in n['id']:
        print(f'  {n["id"]} -> {n["data"]["nodeMeta"]["aliasName"]}')
        outputs = n['data'].get('outputs', [])
        for o in outputs:
            desc = o.get('schema', {}).get('description', '(无描述)')
            req = o.get('schema', {}).get('required', '?')
            print(f'    字段: {o["name"]} | 必填: {req} | 描述: {desc[:200]}')
        np = n['data']['nodeParam']
        print(f'    answerType: {np.get("answerType","?")} | directAnswer: {np.get("directAnswer","?")}')
        print(f'    question 长度: {len(np.get("question",""))} 字符')
        print()