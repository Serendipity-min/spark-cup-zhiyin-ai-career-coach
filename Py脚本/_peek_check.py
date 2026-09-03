# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

# 自检清单位置
idx = t.find('自检清单')
print('自检清单位置:', idx)
print(t[idx:idx+1200])
