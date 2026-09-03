# -*- coding: utf-8 -*-
"""
精确核验 V3.7test 文件夹下 14 个测试样本的可视化条一致性：
1. 提取所有 [■□]+ / [◆◇]+ / [━─]+ 形式的可视化条
2. 检查长度是否符合规范（评分条=20格，差距条=10格）
3. 检查评分表中"评分X.X"与紧邻■数量是否满足 ■=评分×2
4. 检查差距表中"差距X.X"与紧邻◆数量是否满足 ◆=差距（10格制，四舍五入）
5. 输出所有异常
"""
import re
import os
import glob
import sys

sys.stdout.reconfigure(encoding="utf-8")

folder = r"E:\workbuddy_projrct\星火杯\测试\V3.7test"
files = sorted(glob.glob(os.path.join(folder, "*.txt")))

bar_pattern = re.compile(r'\[([■□◆◇━─]+)\]')

issues = []
summary = []

for fp in files:
    name = os.path.basename(fp)
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    bars = bar_pattern.findall(content)
    block_bars = [b for b in bars if set(b) <= set('■□')]
    diamond_bars = [b for b in bars if set(b) <= set('◆◇')]
    line_bars = [b for b in bars if set(b) <= set('━─')]

    file_issues = []

    for b in block_bars:
        length = len(b)
        if length != 20:
            file_issues.append(f"评分条长度异常: '{b}' 长度={length} (应为20)")

    for b in diamond_bars:
        length = len(b)
        if length != 10:
            file_issues.append(f"差距条长度异常: '{b}' 长度={length} (应为10)")

    lens = {}
    for b in line_bars:
        length = len(b)
        lens.setdefault(length, []).append(b)
    if len(lens) > 1:
        detail = ", ".join([f"{l}格x{len(v)}个" for l, v in sorted(lens.items())])
        file_issues.append(f"进度条长度不统一: {detail}")

    # 数值一致性检查：查找 "X.X/10" 后紧跟的 [■■...] 条
    score_bar_pattern = re.compile(r'(\d+\.\d)\s*/\s*10[^\[\n]{0,15}\[([■□]+)\]')
    for m in score_bar_pattern.finditer(content):
        score = float(m.group(1))
        bar = m.group(2)
        if len(bar) == 20:
            expected_filled = round(score * 2)
            actual_filled = bar.count('■')
            if abs(expected_filled - actual_filled) > 0:
                file_issues.append(
                    f"评分不一致: 评分{score}/10 应有■={expected_filled}个，实际■={actual_filled}个 -> [{bar}]"
                )

    # 差距一致性：查找 "差距X.X" 或独立差距数值后紧跟 [◆◆...] 条 (10格)
    gap_bar_pattern = re.compile(r'(\d+\.\d)\s*[^\[\n]{0,10}\[([◆◇]+)\]')
    for m in gap_bar_pattern.finditer(content):
        gap = float(m.group(1))
        bar = m.group(2)
        if len(bar) == 10:
            expected_filled = round(gap)
            actual_filled = bar.count('◆')
            if abs(expected_filled - actual_filled) > 0:
                file_issues.append(
                    f"差距不一致: 差距{gap} 应有◆={expected_filled}个，实际◆={actual_filled}个 -> [{bar}]"
                )

    summary.append((name, len(block_bars), len(diamond_bars), len(line_bars), len(file_issues)))
    if file_issues:
        issues.append((name, file_issues))

print("=" * 70)
print("汇总：各文件可视化条数量")
print("=" * 70)
for name, nb, nd, nl, ni in summary:
    flag = "[X]" if ni else "[OK]"
    print(f"{flag} {name:45s} 评分条:{nb:2d} 差距条:{nd:2d} 进度条:{nl:2d} 问题数:{ni}")

print()
print("=" * 70)
print("详细问题列表")
print("=" * 70)
if not issues:
    print("未发现异常")
else:
    for name, file_issues in issues:
        print(f"\n【{name}】")
        for iss in file_issues:
            print(f"  - {iss}")
