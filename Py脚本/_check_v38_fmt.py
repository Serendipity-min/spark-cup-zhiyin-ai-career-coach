# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    text = f.read()

# 检查 \n vs \\n 在 v3.8 文件中的实际格式
idx = text.find('规则 0')
section = text[idx:idx+300]
print('section repr (前 300 字):')
print(repr(section))
print()
print('section 实际显示:')
print(section)
