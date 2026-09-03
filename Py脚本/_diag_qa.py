# -*- coding: utf-8 -*-
"""诊断 QA 节点的字段提取配置，找到导致提取失败的根因"""
import yaml, sys, json
sys.stdout.reconfigure(encoding='utf-8')

fn = r'E:\workbuddy_projrct\星火杯\职引_v3.1_FINAL.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

for nid in ['question-answer::c17e1d8f', 'question-answer::8b7f2f5a', 'question-answer::3f928444']:
    n = next(x for x in d['flowData']['nodes'] if x['id'] == nid)
    label = n['data']['nodeMeta']['aliasName']
    np = n['data']['nodeParam']
    print(f'\n{"="*60}')
    print(f'【{label}】')
    print(f'{"="*60}')

    # 字段提取配置：outputs 里的 schema.description
    outputs = n['data'].get('outputs', [])
    print(f'\n--- 字段提取配置（schema.description）---')
    for o in outputs:
        name = o['name']
        desc = o.get('schema', {}).get('description', '(无描述)')
        required = o.get('schema', {}).get('required', '?')
        print(f'  字段: {name} | 必填: {required} | 描述: {desc[:150]}')

    # 其他关键参数
    print(f'\n--- 其他关键参数 ---')
    print(f'  answerType: {np.get("answerType", "?")}')
    print(f'  directAnswer: {np.get("directAnswer", "?")}')
    print(f'  optionAnswer (样本选项数): {len(np.get("optionAnswer", []))}')
    if np.get('optionAnswer'):
        print(f'    样本: {np["optionAnswer"][:1]}')

    # temperature
    print(f'  temperature: {np.get("temperature", "?")}')
    print(f'  modelName: {np.get("modelName", "?")}')

    # question 长度
    q = np.get('question', '')
    print(f'  question 长度: {len(q)} 字符')