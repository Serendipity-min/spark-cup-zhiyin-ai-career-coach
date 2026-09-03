# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.9_精细修复版.yml', encoding='utf-8') as f:
    text = f.read()

# 检查关键能力模板
for kw in ['（能力 1）', '[■■■■□□□□□]', '[■■■■■■■□□]', '[■■■□□□□□□]', '[□□□□□□□□□]', '[■■■■■■■□□]', '[━━────────]', '[━─────────]']:
    n = text.count(kw)
    print(f'[{kw}] 出现 {n} 次')
