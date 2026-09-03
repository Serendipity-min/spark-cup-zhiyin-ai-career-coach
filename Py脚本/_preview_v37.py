# -*- coding: utf-8 -*-
"""模拟 v3.7 实际输出（开发工程师报告）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

def bar(score, width=20):
    filled = round(score / 10 * width)
    return '[' + '■' * filled + '□' * (width - filled) + ']'

def gap_bar(gap, width=10):
    if gap <= 0:
        return '[已达标]'
    return '[' + '◆' * gap + '◇' * (width - gap) + ']'

def week_bar(week_num):
    return '[' + '━' * week_num + '─' * (10 - week_num) + ']'

print('# 软件开发工程师 能力诊断报告')
print()
print('## 二、能力现状评估')
print()
print('| 能力维度 | 评分 | 可视化 |')
print('|---------|------|--------|')
for dim, score in [
    ('编程语言与算法', 3.5),
    ('计算机基础', 1.0),
    ('项目工程实践', 4.0),
    ('代码质量', 2.5),
    ('调试能力', 3.0),
    ('学习能力', 6.0),
]:
    print(f'| {dim} | {score}/10 | {bar(score)} |')

print()
print('## 三、关键差距分析')
print()
print('| 能力 | 你的水平 | 岗位要求 | 差距可视化 |')
print('|------|---------|---------|-----------|')
for d, mine, need, g in [
    ('编程语言', 3.5, 8.0, 4.5),
    ('代码质量', 2.5, 7.0, 4.5),
    ('计算机基础', 1.0, 7.5, 6.5),
]:
    print(f'| {d} | {mine}/10 | {need}/10 | {gap_bar(round(g))} ({g}) |')

print()
print('## 四·补、四周行动时间线')
print()
print('| 周次 | 重点任务 | 完成进度 |')
print('|------|---------|---------|')
for w, t in [
    (1, '建立算法刷题习惯'),
    (2, 'Excel 强化 + 重构项目'),
    (3, '学习计算机基础'),
    (4, '投递实习 + 模拟面试'),
]:
    print(f'| 第{w}周 | {t} | {week_bar(w)} {w*10}% |')

print()
print('## 六、整体评分与寄语')
print()
print('- 综合能力评分：3.3/10')
print(f'- 综合能力可视化：{bar(3.3, 10)}')
print('- 校招竞争力评级：C（一般）')

print()
print('## 七、能力成长路径')
print()
print('| 维度 | 现在 | 4周后 | 提升 |')
print('|------|------|-------|------|')
for d, now, future in [
    ('编程语言', 3.5, 6.0),
    ('计算机基础', 1.0, 4.0),
    ('项目实践', 4.0, 7.0),
    ('代码质量', 2.5, 5.5),
    ('调试能力', 3.0, 6.0),
]:
    delta = future - now
    print(f'| {d} | {now}/10 {bar(now)} | {future}/10 {bar(future)} | ↑{delta} |')