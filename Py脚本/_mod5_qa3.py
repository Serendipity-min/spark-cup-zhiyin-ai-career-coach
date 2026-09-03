# -*- coding: utf-8 -*-
import yaml, json, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'e:\Chrome\职引 · AI职业诊断官.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 问答 3
n = next(n for n in d['flowData']['nodes'] if n['id'] == 'question-answer::3f928444-790d-4fd6-a5d6-471ccd3bc5d3')
print('=== 询问实践经验 nodeParam.question ===')
print(n['data']['nodeParam']['question'])
print()
print('=== outputs ===')
for o in n['data']['outputs']:
    print(json.dumps(o, ensure_ascii=False, indent=2))