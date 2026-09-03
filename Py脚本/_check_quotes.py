# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    text = f.read()

# 找双引号位置
idx = text.find('长度固定')
print('长度固定位置:', idx)
# 找前后引号
print('前后 60 字 repr:')
print(repr(text[idx-3:idx+30]))

# 检测是中文引号还是英文引号
# 中：U+201C（左双引号），U+201D（右双引号）
# 英："（U+0022）
section = text[idx-3:idx+30]
for c in section:
    if c in '""「」':
        print(f'  字符 {repr(c)}: U+{ord(c):04X}')
