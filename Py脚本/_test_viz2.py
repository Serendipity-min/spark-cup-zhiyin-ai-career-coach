# -*- coding: utf-8 -*-
"""
测试纯文本可视化方案 - 输出到文件供查看
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================
# 方案 A：能力维度条形图
# ============================================================
def bar_chart_horizontal(items, max_width=20):
    print('### 方案 A：能力维度条形图')
    print()
    print('| 能力维度 | 当前水平 | 可视化 |')
    print('|---------|---------|--------|')
    for label, value in items:
        filled = int(value / 10 * max_width)
        bar = '#' * filled + '-' * (max_width - filled)
        print(f'| {label} | {value}/10 | [{bar}] |')

bar_chart_horizontal([
    ('SQL 数据库查询', 3.0),
    ('Python 数据分析', 7.0),
    ('Excel 高级应用', 8.0),
    ('业务理解', 5.0),
    ('数据可视化', 4.0),
    ('沟通表达', 8.5),
])
print()

# ============================================================
# 方案 B：4 周行动时间线
# ============================================================
print('### 方案 B：4 周行动时间线')
print()
print('| 周次 | 重点任务 | 完成度 |')
print('|------|---------|--------|')
weeks = [
    ('W1 第1周', '掌握核心工具链（Python + SQL）', '[########..] 80%'),
    ('W2 第2周', '完成第一个完整的数据分析项目', '[######....] 60%'),
    ('W3 第3周', '制作个人作品集 + GitHub', '[####......] 40%'),
    ('W4 第4周', '投递实习 + 模拟面试', '[##........] 20%'),
]
for w in weeks:
    print(f'| {w[0]} | {w[1]} | `{w[2]}` |')
print()

# ============================================================
# 方案 C：能力差距对比
# ============================================================
print('### 方案 C：能力差距对比')
print()
print('| 能力维度 | 你的水平 | 岗位要求 | 差距 |')
print('|---------|---------|---------|------|')
items = [
    ('SQL', 3, 9, 6),
    ('Python', 7, 8, 1),
    ('Excel', 8, 7, -1),
    ('业务理解', 5, 9, 4),
    ('数据可视化', 4, 8, 4),
]
for label, mine, need, gap in items:
    bar_len = max(0, gap)
    bar = '+' * bar_len + '-' * max(0, 5 - bar_len) if bar_len > 0 else '无'
    print(f'| {label} | {mine}/10 | {need}/10 | [{bar}] ({gap}) |')
print()

# ============================================================
# 方案 D：ASCII 雷达图（简化）
# ============================================================
print('### 方案 D：简化雷达图')
print()
print('```')
labels = ['SQL', 'Python', 'Excel', '业务', '沟通', '学习']
values = [3, 7, 8, 5, 8.5, 9]
for level in [10, 8, 6, 4, 2]:
    row = f'{level:2d}|'
    for v in values:
        if v >= level:
            row += ' ### |'
        elif v >= level - 1.5:
            row += '  *  |'
        else:
            row += '     |'
    print(row)
print('  +' + '-----+' * len(labels))
print('   ' + '  '.join([f'{l:>4}' for l in labels]))
print('```')
print()

print('=' * 60)
print('结论：')
print('  - 方案 A：稳定、清晰，最推荐用于"能力现状评估"')
print('  - 方案 B：4 周进度最直观')
print('  - 方案 C：差距对比最专业')
print('  - 方案 D：视觉效果好，但符号兼容性需测试')
print()
print('组合方案：报告嵌入 A+B+C 三张图表')