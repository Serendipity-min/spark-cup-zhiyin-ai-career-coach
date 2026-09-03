# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml', encoding='utf-8') as f:
    text = f.read()

# 七节10格模板搜索
print('=== 七节成长路径模板实际内容 ===')
idx = text.find('（能力 1）')
if idx < 0:
    idx = text.find('能力 1')
if idx > 0:
    print(text[idx:idx+500])
else:
    print('未找到能力1关键字')
    # 找 七节
    idx = text.find('### 七')
    if idx > 0:
        print(text[idx:idx+1500])

print()
print('=== user template 警告实际内容 ===')
idx = text.find('可视化字符提醒')
if idx < 0:
    idx = text.find('可视化规范警告')
if idx > 0:
    print(text[max(0,idx-50):idx+600])
else:
    print('未找到警告关键字')
