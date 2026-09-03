# -*- coding: utf-8 -*-
"""V3.9 报告审核 - 互联网内容审核"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# 从报告中提取关键数据
sec2_data = [
    ('信息甄别与风险判断', 4.5, '[■■■■■■■■■□□□□□□□□□□]'),
    ('规则理解与执行', 3.0, '[■■■■■■□□□□□□□□□□□□□□]'),
    ('内容理解与分析', 5.5, '[■■■■■■■■■■■□□□□□□□□]'),
    ('数据处理与报告', 2.0, '[■■■■□□□□□□□□□□□□□□□□]'),
    ('抗压与情绪管理', 4.0, '[■■■■■■■■□□□□□□□□□□□□]'),
    ('沟通协作', 5.0, '[■■■■■■■■■■□□□□□□□□□□]'),
]

sec3_data = [
    ('信息甄别与风险判断', 4.0, '[◆◆◆◆◇◇◇◇◇◇]'),
    ('数据处理与报告', 5.0, '[◆◆◆◆◆◇◇◇◇◇]'),
    ('内容理解与分析', 2.5, '[◆◆◆◇◇◇◇◇◇◇]'),
]

sec4_data = [
    ('P0', '[━━━━━━━━━━]'),
    ('P1', '[━━━━━━━───]'),
    ('P2', '[━━━━━─────]'),
    ('P3', '[━━━───────]'),
]

timeline_data = [
    ('第1周', '[━─────────] 20%', 1),
    ('第2周', '[━━────────] 40%', 2),
    ('第3周', '[━━━───────] 60%', 3),
    ('第4周', '[━━━━──────] 80%', 4),
    ('第4周末', '[━━━━━─────] 100%', 5),
]

sec6_score = 4.2
sec6_bar = '[■■■■□□□□□□]'

sec7_data = [
    ('信息甄别与风险判断', 4.5, '[■■■■■□□□□□]', 7.0, '[■■■■■■■□□□]'),
    ('规则理解与执行', 3.0, '[■■■□□□□□□]', 6.0, '[■■■■■■□□□□]'),
    ('内容理解与分析', 5.5, '[■■■■■■□□□□]', 7.5, '[■■■■■■■□□□]'),
    ('数据处理与报告', 2.0, '[■■□□□□□□□□]', 5.5, '[■■■■■■□□□□]'),
    ('抗压与情绪管理', 4.0, '[■■■■□□□□□□]', 5.0, '[■■■■■□□□□□]'),
]

print('=' * 70)
print(' V3.9 报告审核 - 互联网内容审核')
print('=' * 70)

issues = []

# 二节
print('\n【第二节：能力现状评估】')
for name, score, bar in sec2_data:
    expected_solid = round(score * 2)
    actual_solid = bar.count('■')
    actual_total = bar.count('■') + bar.count('□')
    expected_total = 20

    ok = actual_solid == expected_solid and actual_total == expected_total
    flag = '✅' if ok else '❌'
    print(f'  {flag} {name}: 评分{score}, ■={actual_solid}(预期{expected_solid}), 总长={actual_total}(预期{expected_total})')
    if not ok:
        issues.append(f'二节: {name} ■数/总长不符')

# 三节
print('\n【第三节：关键差距】')
for name, gap, bar in sec3_data:
    expected_diamond = round(gap)
    actual_diamond = bar.count('◆')
    actual_total = bar.count('◆') + bar.count('◇')

    ok = actual_diamond == expected_diamond and actual_total == 10
    flag = '✅' if ok else '❌'
    print(f'  {flag} {name}: 差距{gap}, ◆={actual_diamond}(预期{expected_diamond}), 总长={actual_total}(预期10)')
    if not ok:
        issues.append(f'三节: {name} ◆数不符')

# 四节
print('\n【第四节：补齐方案周进度条】')
for name, bar in sec4_data:
    actual_thick = bar.count('━')
    actual_total = bar.count('━') + bar.count('─')

    ok = actual_total == 10
    flag = '✅' if ok else '❌'
    print(f'  {flag} {name}: 总长={actual_total}(预期10), ━={actual_thick}')
    if not ok:
        issues.append(f'四节: {name} 总长不是10')

# 四·补
print('\n【四·补、四周行动时间线】')
for name, line, week_num in timeline_data:
    m = re.search(r'\[([━─]+)\]', line)
    if not m:
        print(f'  ❌ {name}: 未找到进度条')
        continue
    bar = m.group(1)
    actual_thick = bar.count('━')
    actual_total = len(bar)
    expected_thick = week_num

    ok = actual_total == 10 and actual_thick == expected_thick
    flag = '✅' if ok else '❌'
    print(f'  {flag} {name}: 总长={actual_total}(预期10), ━={actual_thick}(预期{expected_thick})')
    if not ok:
        issues.append(f'四·补: {name} ━数不符')

# 六节
print('\n【第六节：综合能力评分】')
score = sec6_score
bar = sec6_bar
expected_solid = round(score)
actual_solid = bar.count('■')
actual_total = bar.count('■') + bar.count('□')

ok = actual_total == 10 and actual_solid == expected_solid
flag = '✅' if ok else '❌'
print(f'  {flag} 综合能力 {score} 分: ■={actual_solid}(预期{expected_solid}), 总长={actual_total}(预期10)')
if not ok:
    issues.append(f'六节: 综合能力 ■数不符')

# 七节
print('\n【第七节：成长路径】')
for name, start_score, start_bar, end_score, end_bar in sec7_data:
    expected_start = round(start_score)
    expected_end = round(end_score)

    actual_start = start_bar.count('■')
    actual_end = end_bar.count('■')

    start_total = start_bar.count('■') + start_bar.count('□')
    end_total = end_bar.count('■') + end_bar.count('□')

    ok_start = actual_start == expected_start and start_total == 10
    ok_end = actual_end == expected_end and end_total == 10
    flag = '✅✅' if ok_start and ok_end else '❌'
    print(f'  {flag} {name}: 起点[{start_score}分, ■={actual_start}/{expected_start}, 总长={start_total}] → 终点[{end_score}分, ■={actual_end}/{expected_end}, 总长={end_total}]')
    if not ok_start:
        issues.append(f'七节: {name} 起点不符')
    if not ok_end:
        issues.append(f'七节: {name} 终点不符')

# 总评
print('\n' + '=' * 70)
print(' 审核总结')
print('=' * 70)
if not issues:
    print('\n  ✅✅✅ 全部通过！V3.9 可视化问题已彻底修复！')
else:
    print(f'\n  ❌ 发现 {len(issues)} 处问题：')
    for i, issue in enumerate(issues, 1):
        print(f'    {i}. {issue}')