# -*- coding: utf-8 -*-
"""编辑参赛信息表 - 精确XML替换版"""
import sys, os, zipfile, shutil, re
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表.docx'
DST = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表_职引已填.docx'
WORK = r'c:\Users\Serendipity\OneDrive\桌面\_docx_work'

if os.path.exists(WORK):
    shutil.rmtree(WORK)
os.makedirs(WORK)

with zipfile.ZipFile(SRC, 'r') as z:
    z.extractall(WORK)

doc_path = os.path.join(WORK, 'word', 'document.xml')
with open(doc_path, 'r', encoding='utf-8') as f:
    xml = f.read()

orig_xml = xml  # keep for comparison

# ─── 替换 1: 作品全称 XXXX ───────────────────────────────
# Cell[2] = gridSpan=4, 两个连续的 <w:t>XX</w:t>
# 精确替换：找到这个双XX块并替换为新名称
old_xxxx = (
    '<w:t>XX</w:t>'
    '</w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" '
    'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/>'
    '<w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr>'
    '<w:t>XX</w:t>'
)
new_xxxx = '<w:t>职引 · AI就业竞争力诊断智能体</w:t>'
if old_xxxx in xml:
    xml = xml.replace(old_xxxx, new_xxxx, 1)
    print('✓ 作品全称 → 职引 · AI就业竞争力诊断智能体')
else:
    print('✗ 作品全称 XXXX 未找到，尝试备用...')
    # 备用：找 gridSpan=4 后紧跟的XX
    m = re.search(r'(<w:gridSpan w:val="4"/>.*?<w:t>)XX(</w:t>.*?<w:t>)XX(</w:t>)', xml, re.DOTALL)
    if m:
        xml = xml[:m.start()] + m.group(1) + '职引 · AI就业竞争力诊断智能体' + m.group(3) + xml[m.end():]
        print('✓ 作品全称 → 备用方案成功')
    else:
        print('✗ 作品全称替换失败')

# ─── 替换 2: 团队名称 XX团队 ─────────────────────────────
# Cell[4] = gridSpan=2, <w:t>XX</w:t><w:t>团队</w:t>
# 只需改第一个XX为职引
old_team = (
    '<w:t>XX</w:t>'
    '</w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" '
    'w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/>'
    '<w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr>'
    '<w:t>团队</w:t>'
)
new_team = '<w:t>职引</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/><w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr><w:t>星火团队</w:t>'
if old_team in xml:
    xml = xml.replace(old_team, new_team, 1)
    print('✓ 团队名称 → 职引星火团队')
else:
    print('✗ 团队名称 XX团队 未找到，尝试备用...')
    m2 = re.search(r'(<w:gridSpan w:val="2"/>.*?<w:t>)XX(</w:t>.*?<w:t>)团队(</w:t>)', xml, re.DOTALL)
    if m2:
        xml = xml[:m2.start()] + m2.group(1) + '职引' + m2.group(2) + '星火' + m2.group(3) + xml[m2.end():]
        print('✓ 团队名称 → 备用方案成功')
    else:
        print('✗ 团队名称替换失败')

# ─── 替换 3: 作品简介示例 ────────────────────────────────
old_jj = '面向大学生的课程规划助手，可根据课表自动生成学习计划，支持考试倒计时提醒。'
new_jj = '面向大学生的AI就业竞争力诊断助手，通过多轮对话深挖用户能力画像，输出可视化差距报告与4周冲刺计划。'
if old_jj in xml:
    xml = xml.replace(old_jj, new_jj)
    print('✓ 作品简介 → 已替换')
else:
    print('✗ 作品简介示例未找到')

# ─── 替换 4: 使用说明示例 ────────────────────────────────
old_sy = '用户输入课表或考试日期，助手会自动生成每日学习计划，并按优先级推送任务提醒。'
new_sy = '用户输入目标岗位，系统联网抓取实时JD，多轮对话收集背景信息，自动生成含雷达图、周计划的诊断报告。'
if old_sy in xml:
    xml = xml.replace(old_sy, new_sy)
    print('✓ 使用说明 → 已替换')
else:
    print('✗ 使用说明示例未找到，尝试模糊匹配...')
    # 找助手会自动生成
    idx = xml.find('助手会自动生成')
    if idx >= 0:
        print(f'  找到上下文: {repr(xml[idx-50:idx+200])}')

# ─── 替换 5: 创新点示例 ────────────────────────────────
old_cx = '1. 结合用户历史数据，提供个性化学习节奏建议；2. 一键生成可导出的 PDF 学习计划表。'
new_cx = '1. 首创「AI诊断+验证行双保险」流程，确保可视化数据精确可信；2. 联网实时抓取招聘JD，保证分析基于最新市场需求。'
if old_cx in xml:
    xml = xml.replace(old_cx, new_cx)
    print('✓ 创新点 → 已替换')
else:
    print('✗ 创新点示例未找到，尝试模糊匹配...')
    idx = xml.find('PDF 学习计划表')
    if idx >= 0:
        print(f'  找到: {repr(xml[idx-200:idx+200])}')

# ─── 替换 6: 队员占位符 → 待补充 ──────────────────────
队员_list = ['队员1姓名', '队员2姓名', '队员3姓名', '队员4姓名', '队员5姓名']
for name in 队员_list:
    if name in xml:
        xml = xml.replace(f'<w:t>{name}</w:t>', f'<w:t>（待补充）</w:t>')
        print(f'✓ {name} → （待补充）')
    else:
        print(f'✗ {name} 未找到')

# ─── 保存 ───────────────────────────────────────────────
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(xml)

# ─── 打包 ───────────────────────────────────────────────
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root_dir, dirs, files in os.walk(WORK):
        for file in files:
            fp = os.path.join(root_dir, file)
            arcname = os.path.relpath(fp, WORK)
            zout.write(fp, arcname)

print(f'\n✅ 输出: {DST}')

# ─── 验证 ───────────────────────────────────────────────
with zipfile.ZipFile(DST, 'r') as zv:
    x = zv.read('word/document.xml').decode('utf-8')
    checks = [
        ('职引 · AI就业竞争力诊断智能体', '作品全称'),
        ('职引星火团队', '团队名称'),
        ('就业竞争力', '简介关键词'),
        ('差距报告', '简介关键词'),
        ('冲刺计划', '简介关键词'),
        ('联网', '创新点关键词'),
        ('待补充', '队员占位符'),
    ]
    print('\n验证:')
    all_ok = True
    for kw, label in checks:
        found = kw in x
        print(f'  {"✓" if found else "✗"} {label}: {kw}')
        if not found:
            all_ok = False
    if all_ok:
        print('\n🎉 全部验证通过！')
    else:
        print('\n⚠ 有字段验证失败，请检查上方')
