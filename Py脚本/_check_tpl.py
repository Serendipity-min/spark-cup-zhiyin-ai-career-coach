# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\workbuddy_projrct\星火杯\职引_v3.7.yml', encoding='utf-8') as f:
    t = f.read()

idx = t.find('systemTemplate:')
print('systemTemplate位置:', idx)
# 取 systemTemplate 字符串值
import re
m = re.search(r'systemTemplate:\s*"', t)
if m:
    start = m.end()
    # 字符串以 " 结束，下一个 \n
    end = t.find('"\n        respFormat', start)
    if end < 0:
        end = t.find('"\n      respFormat', start)
    raw = t[start:end]
    print('字符串前200字（repr）:')
    print(repr(raw[:200]))
    print('字符串包含的换行符类型:')
    print('  \\n(字面反斜杠n)出现:', raw.count('\\n'))
    print('  \\u00a0 出现:', raw.count('\u00a0'))
    print('  真换行符出现:', raw.count('\n'))
    print('  \\\\n(双反斜杠)出现:', raw.count('\\\\n'))
