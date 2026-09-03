# -*- coding: utf-8 -*-
"""
候选进度条样式 - 在 Markdown 中渲染测试
目标：找出在星火平台（一般 Markdown 渲染器）下最好看、最稳定的方案
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def show_case(name, score, width=10):
    """统一展示一个评分的所有方案"""
    print(f'\n=== 评分 {score}/10 (满分 {width}) ===\n')

    # 方案 1：纯 ASCII（丑但稳定）
    filled = round(score / 10 * width)
    bar1 = '[' + '#' * filled + '-' * (width - filled) + ']'
    print(f'方案1 ASCII    : {bar1}')

    # 方案 2：emoji 块
    bar2 = '[' + '🟩' * filled + '⬜' * (width - filled) + ']'
    print(f'方案2 彩色块    : {bar2}')

    # 方案 3：纯文本+百分比
    pct = int(score / 10 * 100)
    bar3 = '█' * filled + '░' * (width - filled)
    print(f'方案3 块字符    : [{bar3}] {pct}%')

    # 方案 4：Unicode 方块
    bar4 = '▰' * filled + '▱' * (width - filled)
    print(f'方案4 Unicode方块: [{bar4}]')

    # 方案 5：箭头形
    bar5 = '▶' * filled + '▷' * (width - filled)
    print(f'方案5 箭头形    : [{bar5}]')

    # 方案 6：纯中文（中文方块）
    bar6 = '■' * filled + '□' * (width - filled)
    print(f'方案6 中方块    : [{bar6}]')

    # 方案 7：圆点
    bar7 = '●' * filled + '○' * (width - filled)
    print(f'方案7 圆点      : [{bar7}]')

    # 方案 8：星号
    bar8 = '★' * filled + '☆' * (width - filled)
    print(f'方案8 星号      : [{bar8}]')

    # 方案 9：横线+勾
    bar9 = '━' * filled + '─' * (width - filled)
    print(f'方案9 粗细线    : [{bar9}]')

    # 方案 10：双线
    bar10 = '═' * filled + '─' * (width - filled)
    print(f'方案10 双线     : [{bar10}]')


# 评分示例
print('=' * 60)
print('进度条样式对比 - 7个评分档位')
print('=' * 60)
for score in [1.0, 2.5, 3.5, 5.0, 6.5, 8.0, 9.5]:
    show_case(str(score), score, 10)

print('\n\n' + '=' * 60)
print('渲染兼容性分析：')
print('=' * 60)
print('''
方案1 (#-)        : 100% 兼容，太丑 ← 我们现在用的
方案2 (🟩⬜)       : 大多数平台支持，但 emoji 在某些终端显示不一致
方案3 (█░)        : 部分渲染器支持 █ 字符，▒░ 兼容性较差
方案4 (▰▱)        : 较新 Unicode，移动端兼容好
方案5 (▶▷)        : 箭头字符广泛支持
方案6 (■□)        : 100% 兼容 ← ★ 推荐
方案7 (●○)        : 100% 兼容
方案8 (★☆)        : 100% 兼容但语义不当（星星通常代表评分）
方案9 (━─)        : Unicode 横线，兼容性好
方案10(═─)        : 双线，PC 端美观

★ 最优组合：方案6 ■□（主）+ 方案4 ▰▱（备选）+ 方案10 ═（双线背景）
''')

# 完整报告片段预览
print('\n' + '=' * 60)
print('完整报告片段预览 - 改造后效果')
print('=' * 60)
print()

def bar(score, width=20):
    filled = round(score / 10 * width)
    return '[' + '■' * filled + '□' * (width - filled) + ']'

print('## 二、能力现状评估')
print()
print('| 能力维度 | 评分 | 可视化 |')
print('|---------|------|--------|')
evals = [
    ('编程语言与算法', 3.5),
    ('计算机基础', 1.0),
    ('项目工程实践', 4.0),
    ('代码质量', 2.5),
    ('调试能力', 3.0),
    ('学习能力', 6.0),
]
for dim, score in evals:
    print(f'| {dim} | {score}/10 | {bar(score)} |')

print()
print('## 三、关键差距分析')
print()
print('| 能力 | 你的水平 | 岗位要求 | 差距 |')
print('|------|---------|---------|------|')
gaps = [
    ('编程语言', 3.5, 8.0, 4.5),
    ('代码质量', 2.5, 7.0, 4.5),
    ('计算机基础', 1.0, 7.5, 6.5),
]
for d, mine, need, gap in gaps:
    g_filled = round(gap / 10 * 10)
    g_bar = '[' + '◆' * g_filled + '◇' * (10 - g_filled) + ']'
    print(f'| {d} | {mine}/10 | {need}/10 | {g_bar} ({gap}) |')

print()
print('## 四、四周行动时间线')
print()
print('| 周次 | 重点任务 | 完成进度 |')
print('|------|---------|---------|')
for week, task in [
    (1, '建立算法刷题习惯'),
    (2, 'Excel 强化'),
    (3, '完成数据分析项目'),
    (4, '投递实习'),
]:
    filled = week * 2
    bar_str = '[' + '━' * filled + '─' * (10 - filled) + ']'
    pct = week * 20
    print(f'| 第{week}周 | {task} | {bar_str} {pct}% |')