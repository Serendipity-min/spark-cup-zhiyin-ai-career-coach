# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

# 找 能力 1 位置（无括号版）
idx = t.find('能力 1')
print(f'能力 1 位置: {idx}')
if idx > 0:
    print(t[max(0,idx-30):idx+300])
