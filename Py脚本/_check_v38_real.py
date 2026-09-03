# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', 'r', encoding='utf-8') as f:
    text = f.read()

# 找规则 0 起点
idx = text.find('规则 0')
print(f'规则 0 位置: {idx}')
print(f'附近 100 字符 repr:')
print(repr(text[idx:idx+150]))
