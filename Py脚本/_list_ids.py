# -*- coding: utf-8 -*-
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')
fn = r'E:\workbuddy_projrct\星火杯\职引_v3.2_字段提取修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

print('=== v3.2 全部节点 ID ===')
for n in d['flowData']['nodes']:
    print(f'  {n["id"][:60]} -> {n["data"]["nodeMeta"]["aliasName"]}')