# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

for kw in ['[■■□□□□□□□]', '[■■■■□□□□□]', '（能力 1）', '（能力 2）', '能力 1', '10格，严格精确', '可视化字符提醒']:
    print(f'[{kw}] 出现 {t.count(kw)} 次')
