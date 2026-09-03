# -*- coding: utf-8 -*-
"""v3.3 综合验证"""
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.3_死循环修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('=== v3.3 综合验证报告 ===\n')

# 检查所有 3 个 QA 节点
for nid in ['c17e1d8f', '8b7f2f5a', '3f928444']:
    for n in d['flowData']['nodes']:
        if nid in n['id']:
            label = n['data']['nodeMeta']['aliasName']
            np = n['data']['nodeParam']
            da = np.get('directAnswer', {})
            mrc = da.get('maxRetryCounts', '?')
            print(f'【{label}】 maxRetryCounts={mrc}')

# QA3 专项检查
for n in d['flowData']['nodes']:
    if '3f928444' in n['id']:
        print()

        # 1. skills 字段描述
        for o in n['data']['outputs']:
            if o['name'] == 'skills':
                desc = o['schema']['description']
                print(f'skills 字段描述:')
                print(f'  {desc}')
                print(f'  ✅ 包含"直接转述": {"直接转述" in desc}')
                print(f'  ✅ 无工具示例: {"如" not in desc}')
                print()

        # 2. question 全文检查
        q = n['data']['nodeParam']['question']

        checks = [
            ('[岗位相关工具', False, '无残留占位符'),
            ('SQL、Python、Tableau', False, '无 SQL/Python/Tableau 硬编码'),
            ('如 word / Python / Excel', False, '无 Word/Python/Excel 硬编码'),
            ('有哪些就列哪些', True, '有通用化工具提示'),
            ('告诉我你掌握的与目标岗位相关的工具或技能即可。如果暂无，回复"暂无"', True, '追问通用化'),
            ('如果暂无，直接回复"暂无"', True, '无格式强制要求'),
        ]
        print('question 文本检查:')
        for kw, expect, note in checks:
            found = kw in q
            ok = '✅' if found == expect else '❌'
            print(f'  {ok} {note}: "{kw[:40]}"')

        print('\nquestion 完整工具部分:')
        idx = q.find('**2.')
        print(q[idx:idx+250])

        # 3. 追问部分
        retry_keywords = ['请补充你掌握的', '请补充你描述的', '请补充你提及的']
        print('\n追问提示检查:')
        found_retry = any(k in q for k in retry_keywords)
        print(f'  {"✅ 无追问格式要求" if not found_retry else "⚠️ 可能存在追问"}')

        break

print('\n=== ✅ v3.3 验证完成 ===')