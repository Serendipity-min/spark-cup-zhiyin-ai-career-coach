# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    text = f.read()

# 找规则0位置
idx = text.find('规则 0')
print('规则0位置:', idx)
print('---规则0附近内容---')
print(text[idx:idx+1500])
print('---')
