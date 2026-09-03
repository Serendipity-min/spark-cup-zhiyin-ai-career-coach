# -*- coding: utf-8 -*-
"""最终质量确认 - 简化版"""
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.3_死循环修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('=== v3.3 质量确认 ===\n')

for n in d['flowData']['nodes']:
    if '3f928444' not in n['id']:
        continue

    # skills 字段
    for o in n['data']['outputs']:
        if o['name'] == 'skills':
            desc = o['schema']['description']
            print(f'✅ skills 字段: "{desc}"')
            print()

    # question 工具部分
    q = n['data']['nodeParam']['question']
    idx = q.find('**2. 工具和技能')
    snippet = q[idx:idx+250]
    print(f'✅ question 工具格式提示:\n{snippet}\n')

    # 确认没有会导致死循环的内容
    bad_patterns = [
        '如"SQL、Python、Tableau"等',
        '如"暂无"或具体描述',
        '请补充你描述的实习',
        '如 word / Python / Excel',
        '[岗位相关工具',
    ]
    print('死循环风险检查:')
    all_safe = True
    for p in bad_patterns:
        if p in q:
            print(f'  ❌ 危险: {p}')
            all_safe = False
    if all_safe:
        print('  ✅ 无死循环风险内容')
    break

print('\n=== 文件路径 ===')
print(fn)