# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

for kw in ['二节可视化规则','查上方对照表','二节重写','能力现状评估','二节专用']:
    idx = t.find(kw)
    print(f'[{kw}] 位置: {idx}')

idx = t.find('能力现状评估')
if idx > 0:
    print('---上下文---')
    print(t[idx-50:idx+500])
    print('---')
