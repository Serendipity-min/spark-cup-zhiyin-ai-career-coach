# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.7.yml', encoding='utf-8') as f:
    text = f.read()

# 简单测试：用最简单的子串
test1 = "**规则 0：可视化规范**（强制，美观版）"
print('test1 in text:', test1 in text)

# 测试包含 \n 的子串
test2 = "**规则 0：可视化规范**（强制，美观版）" + chr(92) + 'n' + chr(92) + 'n' + "**进度条字符**"
print('test2 in text:', test2 in text)
print('test2 repr:', repr(test2[:80]))

# 找出实际串片段
needle = "**规则 0：可视化规范**"
idx = text.find(needle)
print('找到位置:', idx)
print('片段:')
print(repr(text[idx:idx+80]))
