# -*- coding: utf-8 -*-
"""
按章节分别校验 V3.7test 样本：
- 二、能力现状评估：评分条应为 20 格，且 ■数量 = round(评分*2)
- 三、差距可视化表：差距条应为 10 格，且 ◆数量 = round(差距)（向上取整验证也做）
- 四、补齐方案 P0-P3：周进度可视化条长度是否统一（同一份报告内应统一，一般为10格）
- 七、能力成长路径：起点/终点条应为 10 格，且 ■数量 = round(分数)
"""
import re, os, glob, sys
sys.stdout.reconfigure(encoding="utf-8")

folder = r"E:\workbuddy_projrct\星火杯\测试\V3.7test"
files = sorted(glob.glob(os.path.join(folder, "*.txt")))

bar_re = re.compile(r'\[([■□◆◇━─]+)\]')

def get_section(content, start_marker_list, end_marker_list):
    """粗略截取两个标题之间的文本"""
    start_idx = -1
    for m in start_marker_list:
        idx = content.find(m)
        if idx != -1:
            start_idx = idx
            break
    if start_idx == -1:
        return ""
    end_idx = len(content)
    for m in end_marker_list:
        idx = content.find(m, start_idx + 1)
        if idx != -1:
            end_idx = min(end_idx, idx)
    return content[start_idx:end_idx]

report = []

for fp in files:
    name = os.path.basename(fp)
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    sec2 = get_section(content, ["二、能力现状评估", "二、"], ["三、关键差距", "三、"])
    sec3 = get_section(content, ["三、关键差距", "差距可视化表"], ["四、补齐方案", "四、"])
    sec4 = get_section(content, ["四、补齐方案"], ["四·补", "四.补", "五、面试"])
    sec7 = get_section(content, ["七、能力成长路径", "七、"], ["你的 AI 职业诊断官", "职引顾问", "END_MARKER_NOT_FOUND"])

    problems = []

    # --- 二节：应为20格 ---
    for b in bar_re.findall(sec2):
        if set(b) <= set('■□'):
            if len(b) != 20:
                problems.append(f"[二节] 评分条长度={len(b)} 应为20: [{b}]")

    # 分数与■数一致性（在二节内，查找"X.X" 紧跟着的 bar）
    score_pat = re.compile(r'(\d\.\d)\D{0,20}?\[([■□]{18,22})\]')
    for m in score_pat.finditer(sec2):
        score = float(m.group(1))
        bar = m.group(2)
        if len(bar) == 20:
            expect = round(score * 2)
            actual = bar.count('■')
            if expect != actual:
                problems.append(f"[二节] 分数{score} 应■={expect} 实际■={actual}: [{bar}]")

    # --- 三节：应为10格 ---
    for b in bar_re.findall(sec3):
        if set(b) <= set('◆◇'):
            if len(b) != 10:
                problems.append(f"[三节] 差距条长度={len(b)} 应为10: [{b}]")

    # 差距数值与◆数一致性：查找 "差距 X.X" 或表格行末的 "X.X" 后紧跟的 [◆◆...]
    gap_pat = re.compile(r'差距\D{0,15}?(\d\.\d)\D{0,8}?\[([◆◇]{8,12})\]')
    for m in gap_pat.finditer(sec3):
        gap = float(m.group(1))
        bar = m.group(2)
        if len(bar) == 10:
            expect = round(gap)
            actual = bar.count('◆')
            if expect != actual:
                problems.append(f"[三节] 差距{gap} 应◆={expect} 实际◆={actual}: [{bar}]")

    # --- 四节：周进度条长度是否内部统一 ---
    lens = {}
    for b in bar_re.findall(sec4):
        if set(b) <= set('━─'):
            lens.setdefault(len(b), 0)
            lens[len(b)] += 1
    if len(lens) > 1:
        detail = ", ".join(f"{l}格x{c}" for l, c in sorted(lens.items()))
        problems.append(f"[四节] P0-P3周进度条长度不统一: {detail}")

    # --- 七节：应为10格 ---
    for b in bar_re.findall(sec7):
        if set(b) <= set('■□'):
            if len(b) != 10:
                problems.append(f"[七节] 成长路径条长度={len(b)} 应为10: [{b}]")

    score_pat10 = re.compile(r'(\d\.\d)/10\D{0,10}?\[([■□]{8,12})\]')
    for m in score_pat10.finditer(sec7):
        score = float(m.group(1))
        bar = m.group(2)
        if len(bar) == 10:
            expect = round(score)
            actual = bar.count('■')
            if expect != actual:
                problems.append(f"[七节] 分数{score}/10 应■={expect} 实际■={actual}: [{bar}]")

    report.append((name, problems))

print("=" * 70)
print("按章节精确校验结果")
print("=" * 70)
total_problems = 0
for name, problems in report:
    flag = "[X]" if problems else "[OK]"
    print(f"{flag} {name} 问题数:{len(problems)}")
    total_problems += len(problems)

print()
print("=" * 70)
print(f"详细问题列表 (总计 {total_problems} 处)")
print("=" * 70)
for name, problems in report:
    if problems:
        print(f"\n【{name}】")
        for p in problems:
            print(f"  - {p}")
