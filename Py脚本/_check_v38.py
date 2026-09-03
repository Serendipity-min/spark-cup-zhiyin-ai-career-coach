# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    t = f.read()

for kw in ['二节专用','七节专用','P0-P3专用','自检清单','对照表','禁止12格','10格','精确对照表']:
    n = t.count(kw)
    print(f'{kw}: {n}次')

print('总字符数:', len(t))

# 提取 systemTemplate 长度
import re
matches = re.findall(r'systemTemplate:\s*"', t)
print('systemTemplate出现次数:', len(matches))

# 直接找规则0
idx = t.find('规则 0')
if idx > 0:
    print('规则0 起始位置:', idx)
    print('规则0 后续 200 字:')
    print(t[idx:idx+300])
