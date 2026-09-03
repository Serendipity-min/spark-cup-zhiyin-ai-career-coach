# -*- coding: utf-8 -*-
"""检查 yml 中知识库节点配置"""
import yaml, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

fn = r'E:\workbuddy_projrct\星火杯\职引_v3.2_字段提取修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

for n in d['flowData']['nodes']:
    if 'knowledge-base' in n['id']:
        label = n['data']['nodeMeta']['aliasName']
        np = n['data']['nodeParam']
        print(f'【知识库】{label}')
        kb_id = np.get('knowledgeBaseId', '')
        print(f'  knowledgeBaseId: {kb_id}')

        # 扫描项目目录下所有 json 文件
        kb_dir = r'E:\workbuddy_projrct\星火杯'
        print(f'\n  项目目录下 .json 文件:')
        for f in os.listdir(kb_dir):
            if f.endswith('.json'):
                fp = os.path.join(kb_dir, f)
                size = os.path.getsize(fp)
                print(f'    {f} ({size} bytes)')

        # 尝试读取 knowledge_base.json
        kb_fn = r'E:\workbuddy_projrct\星火杯\knowledge_base.json'
        if os.path.exists(kb_fn):
            with open(kb_fn, encoding='utf-8') as f:
                kb = json.load(f)
            print(f'\n  知识库条目数: {len(kb)}')
            for item in kb[:5]:
                print(f'    Q: {item.get("question","?")[:70]}')
        print()