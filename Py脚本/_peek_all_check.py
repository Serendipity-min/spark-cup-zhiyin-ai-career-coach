# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

# 所有自检清单位置
import re
positions = [m.start() for m in re.finditer('自检清单', t)]
print(f'自检清单出现 {len(positions)} 次, 位置: {positions}')
for i, p in enumerate(positions):
    print(f'\n--- 第{i+1}次 (位置 {p}) ---')
    print(t[p:p+500])
