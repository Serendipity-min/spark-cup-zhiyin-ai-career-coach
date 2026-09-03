# -*- coding: utf-8 -*-
"""编辑参赛信息表 - 最终版（修复团队名 + 替换创新点示例）"""
import sys, zipfile, shutil, re, os
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表_职引已填.docx'
TMP = r'c:\Users\Serendipity\OneDrive\桌面\_docx_work3'
OUT = r'c:\Users\Serendipity\OneDrive\桌面\2026届科大讯飞星火杯大模型应用创新赛参赛作品信息表_职引已填.docx'

if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)

with zipfile.ZipFile(SRC, 'r') as z:
    z.extractall(TMP)

doc_path = os.path.join(TMP, 'word', 'document.xml')
with open(doc_path, 'r', encoding='utf-8') as f:
    xml = f.read()

changes = 0

# ── 1. 修复团队名称：团队 → 星火团队 ──────────────────────────────
# 找「职引」后面最近的那个「团队」（在团队名称单元格内）
# 模式：职引...XX团队 → 职引...XX星火团队
# 但现在的结构是 <w:t>职引</w:t>...<w:t>团队</w:t>
# 我们要找的「团队」是在「职引」之后的第一个「团队」
# 且它前面有斜体灰色格式（和示例字体一致）

# 找「职引</w:t>」的位置
idx_zhin = xml.find('<w:t>职引</w:t>')
if idx_zhin >= 0:
    # 在职引之后找「<w:t>团队</w:t>」（最近的）
    rest = xml[idx_zhin:]
    idx_team = rest.find('<w:t>团队</w:t>')
    if idx_team >= 0:
        # 替换这个「团队」→「星火团队」
        full_pos = idx_zhin + idx_team
        xml = xml[:full_pos] + xml[full_pos:].replace('<w:t>团队</w:t>', '<w:t>星火团队</w:t>', 1)
        print('✓ 团队名称 → 职引星火团队')
        changes += 1
    else:
        print('✗ 未找到职引后的团队文本')
else:
    print('✗ 未找到职引文本')

# ── 2. 替换创新点示例文本 ─────────────────────────────────────────
# 原始XML结构（多段分散）：
# <w:t>1. </w:t></w:r><w:r>...<w:t>结合用户历史数据...</w:t></w:r><w:r>...<w:t>2. </w:t></w:r><w:r>...<w:t>一键生成可导出的</w:t></w:r><w:r>...<w:t xml:space="preserve"> PDF </w:t></w:r><w:r>...<w:t>学习计划表。</w:t></w:r><w:r>...<w:t>"</w:t>
# 合并成一段文本塞入第一个 run

old_cx_runs = [
    '<w:t>1. </w:t>',
    '<w:t>结合用户历史数据，提供个性化学习节奏建议；</w:t>',
    '<w:t>2. </w:t>',
    '<w:t>一键生成可导出的</w:t>',
    '<w:t xml:space="preserve"> PDF </w:t>',
    '<w:t>学习计划表。</w:t>',
]
new_cx_text = '1. 首创「AI诊断+验证行双保险」流程，确保可视化数据精确可信；2. 联网实时抓取招聘JD，保证分析基于最新市场需求。"'

# 找到「1. </w:t>」的位置
idx_1 = xml.find('<w:t>1. </w:t>')
if idx_1 >= 0:
    # 找到包含「1. </w:t>」的整个 <w:r>...</w:r>
    # 向后找 </w:r>
    idx_r_end = xml.find('</w:r>', idx_1)
    if idx_r_end >= 0:
        run_end = idx_r_end + len('</w:r>')
        # 替换为合并后的单段 run（保留原run的rPr）
        # 提取原rPr
        run_start = xml.rfind('<w:r>', 0, idx_1)
        if run_start >= 0:
            # 提取rPr部分
            rpr_start = xml.find('<w:rPr>', run_start)
            if rpr_start >= 0 and rpr_start < idx_1:
                rpr_end = xml.find('</w:rPr>', rpr_start)
                rpr = xml[rpr_start:rpr_end + len('</w:rPr>')]
            else:
                rpr = ''
            
            # 清除斜体（因为不再是示例了）
            rpr = rpr.replace('<w:i/><w:iCs/>', '') if rpr else ''
            # 清除灰色（改回黑色）
            rpr = re.sub(r'<w:color[^/]*/>', '', rpr) if rpr else ''
            
            new_run = f'<w:r>{rpr}<w:t xml:space="preserve">示例："{new_cx_text}</w:t></w:r>'
            
            # 找从「1. 」开始，到「学习计划表。</w:t>」结束的范围
            idx_end = xml.find('<w:t>学习计划表。</w:t>', idx_1)
            if idx_end >= 0:
                # 找到学习计划表后面的 </w:r>
                idx_end_run = xml.find('</w:r>', idx_end)
                if idx_end_run >= 0:
                    segment_end = idx_end_run + len('</w:r>')
                    xml = xml[:idx_1] + new_run + xml[segment_end:]
                    print('✓ 创新点示例 → 已替换')
                    changes += 1
                else:
                    print('✗ 未找到学习计划表后的</w:r>')
            else:
                print('✗ 未找到学习计划表。文本')
        else:
            print('✗ 未找到1.前面的<w:r>')
    else:
        print('✗ 未找到<w:t>1. </w:t>')
else:
    print('✗ 未找到创新点起始标记')

# ── 保存 ──────────────────────────────────────────────
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(xml)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root_dir, dirs, files in os.walk(TMP):
        for file in files:
            fp = os.path.join(root_dir, file)
            zout.write(fp, os.path.relpath(fp, TMP))

print(f'\n✅ 已保存: {OUT}')

# ── 验证 ──────────────────────────────────────────────
with zipfile.ZipFile(OUT, 'r') as zv:
    x = zv.read('word/document.xml').decode('utf-8')
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', x)
    combined = ''.join(texts)
    checks = [
        ('职引 · AI就业竞争力诊断智能体', '作品全称'),
        ('职引星火团队', '团队名称'),
        ('就业竞争力', '简介'),
        ('差距报告', '简介'),
        ('联网', '创新点'),
        ('待补充', '队员占位符'),
        ('首创', '创新点关键词'),
    ]
    print('\n验证:')
    for kw, label in checks:
        found = kw in combined
        print(f'  {"✓" if found else "✗"} {label}: {kw}')

# ── 清理工作目录 ──────────────────────────────────────
shutil.rmtree(TMP)
print('\n🧹 工作目录已清理')
