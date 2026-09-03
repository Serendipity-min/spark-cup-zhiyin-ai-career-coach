# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.7.yml', encoding='utf-8') as f:
    text = f.read()

# 找 systemTemplate 起点
idx = text.find('systemTemplate:')
print('systemTemplate位置:', idx)

# 取 systemTemplate 字符串
start = idx + len('systemTemplate:')
# 跳过空白和开引号
while start < len(text) and text[start] in ' \t':
    start += 1
if text[start] == '"':
    start += 1
end = text.find('"\n', start)
print('字符串长度:', end - start)
raw = text[start:end]

# 看里面的换行情况
print('真换行数:', raw.count('\n'))
print('反斜杠n数 (\\\\n):', raw.count('\\n'))
print('双反斜杠n数 (\\\\\\\\n):', raw.count('\\\\n'))
print('字符串首200字 repr:')
print(repr(raw[:200]))
