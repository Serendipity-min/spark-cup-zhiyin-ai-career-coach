# -*- coding: utf-8 -*-
"""编辑参赛信息表（精确XML替换版）"""
import sys, os, zipfile, shutil, re
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表.docx'
DST = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表_职引已填.docx'
WORK = r'c:\Users\Serendipity\OneDrive\桌面\_docx_work'

if os.path.exists(WORK):
    shutil.rmtree(WORK)
os.makedirs(WORK)

# 1. 解包
with zipfile.ZipFile(SRC, 'r') as z:
    z.extractall(WORK)

# 2. 读取
doc_path = os.path.join(WORK, 'word', 'document.xml')
with open(doc_path, 'r', encoding='utf-8') as f:
    xml = f.read()

# ── 精确替换规则 ─────────────────────────────
replacements = [
    # Cell[2]: XXXX → 职引 · AI就业竞争力诊断智能体
    ('<w:t>XX</w:t>', '<w:t>XX</w:t>'),  # 先跳过，等会精确处理
]

# 先处理 Cell[2] 和 Cell[4]（需要替换两个XX）
# Cell[2] = "<w:t>XX</w:t><w:t>XX</w:t>"
# 替换为 "<w:t>职引 · AI就业竞争力诊断智能体</w:t>"
# 但要避免影响后面的"XX"（智能体编码里也有XX）
# 方案：用更长的上下文片段

# Cell[2] 的完整 XML 是 gridSpan=4 的单元格，两个 <w:t>XX</w:t>
# 找带前后文的最长片段
cell2_pattern = '<w:gridSpan w:val="4"/><w:tcBorders><w:top w:val="single" w:sz="2" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/></w:tcBorders><w:vAlign w:val="center"/></w:tcPr><w:p w14:paraId="739A6358" w14:textId="77777777" w:rsidR="00AE459F" w:rsidRDefault="00000000"><w:pPr><w:ind w:left="66"/><w:jc w:val="center"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/><w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/><w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr><w:t>XX</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/><w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr><w:t>XX</w:t></w:r></w:p>'

old_cell2 = cell2_pattern
new_cell2 = cell2_pattern.replace('<w:t>XX</w:t></w:r><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="仿宋" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:i/><w:iCs/><w:color w:val="A5A5A5" w:themeColor="accent3"/><w:sz w:val="24"/></w:rPr><w:t>XX</w:t>', '<w:t>职引 · AI就业竞争力诊断智能体</w:t>')
# 也去掉i/斜体格式，改成正常黑色
new_cell2 = new_cell2.replace('<w:i/><w:iCs/>', '')

if old_cell2 in xml:
    xml = xml.replace(old_cell2, new_cell2)
    print('✓ 作品全称 → 职引 · AI就业竞争力诊断智能体')
else:
    print('✗ 未找到作品全称段落，尝试备用方案...')
    # 备用：直接替换全部 <w:t>XX</w:t> 但保留第一个
    # 找到 Cell[2] 附近
    idx = xml.find('gridSpan w:val="4"')
    if idx >= 0:
        snippet = xml[idx:idx+2000]
        print('Cell[2] snippet:', repr(snippet[:500]))

# Cell[4]: XX团队 → 职引星火团队
# Cell[4] 是第二个包含gridSpan的单元格，或者直接搜索
# 先找 XX团队 附近的完整片段
idx_team = xml.find('XX团队')
if idx_team >= 0:
    # 找包含团队名称的完整单元格
    print('XX团队 context:', repr(xml[idx_team-300:idx_team+300]))

# 找示例段落 1：作品简介
old_ex1 = '面向大学生的课程规划助手，可根据课表自动生成学习计划，支持考试倒计时提醒。'
new_ex1 = '面向大学生的AI就业竞争力诊断助手，通过多轮对话深挖用户能力画像，输出可视化差距报告与4周冲刺计划。'
if old_ex1 in xml:
    xml = xml.replace(old_ex1, new_ex1)
    print('✓ 作品简介 → 已替换')
else:
    print('✗ 未找到作品简介示例文本')

# 找示例段落 2：使用说明
idx2 = xml.find('用户输入课表或考试日期，助手会自动生成每日学习计划，并按优先级推送任务提醒。')
if idx2 >= 0:
    old_ex2 = '用户输入课表或考试日期，助手会自动生成每日学习计划，并按优先级推送任务提醒。'
    new_ex2 = '用户输入目标岗位，系统联网抓取实时JD，多轮对话收集背景信息，自动生成含雷达图、周计划的诊断报告。'
    xml = xml.replace(old_ex2, new_ex2)
    print('✓ 使用说明 → 已替换')
else:
    print('✗ 未找到使用说明示例文本')
    # 找中文引号包围的文本
    idx2a = xml.find('助手会自动生成')
    if idx2a >= 0:
        print('  找到:", repr(xml[idx2a-200:idx2a+200])')

# 找创新点示例
old_ex3 = '1. 结合用户历史数据，提供个性化学习节奏建议；2. 一键生成可导出的 PDF 学习计划表。'
new_ex3 = '1. 首创「AI诊断+验证行双保险」流程，确保可视化数据精确可信；2. 联网实时抓取招聘JD，保证分析基于最新市场需求。'
if old_ex3 in xml:
    xml = xml.replace(old_ex3, new_ex3)
    print('✓ 创新点 → 已替换')
else:
    # 可能格式略有不同
    idx3 = xml.find('PDF 学习计划表')
    if idx3 >= 0:
        print('创新点 context:', repr(xml[idx3-100:idx3+200]))

# 3. 保存
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(xml)

# 4. 打包
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root_dir, dirs, files in os.walk(WORK):
        for file in files:
            file_path = os.path.join(root_dir, file)
            arcname = os.path.relpath(file_path, WORK)
            zout.write(file_path, arcname)

print(f'\n✅ 输出: {DST}')

# 5. 验证
with zipfile.ZipFile(DST, 'r') as zv:
    x = zv.read('word/document.xml').decode('utf-8')
    checks = [
        ('职引', '职引'),
        ('就业竞争力', '就业竞争力'),
        ('诊断', '诊断'),
        ('差距报告', '差距报告'),
        ('冲刺计划', '冲刺计划'),
        ('创新点', '创新点'),
        ('联网', '联网'),
    ]
    print('\n验证:')
    all_ok = True
    for label, kw in checks:
        found = kw in x
        print(f'  {"✓" if found else "✗"} {label}')
        if not found:
            all_ok = False
    if all_ok:
        print('\n🎉 所有字段验证通过！')
