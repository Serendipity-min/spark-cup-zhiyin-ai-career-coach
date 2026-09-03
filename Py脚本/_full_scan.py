# -*- coding: utf-8 -*-
"""
全量字段检查：确保无任何字段要求用户精准格式匹配
检查维度：
  1. 字段描述（schema.description）— LLM 据此决定提取逻辑
  2. question 提示 — 用户在格式参考中看到的格式要求
  3. 追问提示 — 失败后的追问是否强制格式
"""
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')

fn = r'E:\workbuddy_projrct\星火杯\职引_v3.3_死循环修复.yml'
with open(fn, encoding='utf-8') as f:
    d = yaml.safe_load(f)

# 需要检查的"精准格式关键词"
FORMAT_KEYWORDS = [
    # 强制格式
    '如"',
    '如：',
    '按这个回答',
    '格式参考',
    '按以下格式',
    '严格按',
    '必须按',
    # 工具示例（会导致死循环）
    'SQL、Python',
    'word / Python',
    'Figma',
    'Tableau',
    'Python、',
    '如 word / Python',
    '如"暂无"或',
    '请补充你掌握的与目标岗位',
    '请补充你描述的',
    '请补充你提及的',
    # 强制分隔符
    '格式：',
    '格式:',
    '格式-',
    '格式—',
    # 强制输出格式
    '[',
    '（选填',
    '(选填',
]

# 需要检查的字段节点
QA_IDS = [
    ('c17e1d8f', 'QA1-询问目标岗位'),
    ('8b7f2f5a', 'QA2-询问教育背景'),
    ('3f928444', 'QA3-询问实践经验'),
]

all_issues = []
output_lines = []

def check_text(text, source_label, checks):
    """检查文本是否包含精准格式关键词"""
    found = []
    for kw in checks:
        if kw in text:
            found.append(kw)
    return found

def check_field_desc(desc, field_name, node_label):
    """检查字段描述"""
    issues = []
    desc_lower = desc.lower()
    # 这些关键词如果在描述中，说明强制了格式
    if '如"' in desc and ('"等' in desc or '等"' in desc):
        issues.append(f'包含"如"XX等"格式示例: {desc[:100]}')
    if '按这个回答' in desc or '按以下格式' in desc or '必须按' in desc:
        issues.append(f'包含强制格式指令: {desc[:100]}')
    # 检查是否过于严格
    if 'SQL' in desc or 'Python' in desc or 'Tableau' in desc or 'Figma' in desc:
        issues.append(f'包含具体工具示例，可能导致非IT岗位不匹配: {desc[:100]}')
    return issues

print('=' * 70)
print('全量字段格式安全扫描')
print('=' * 70)

for nid, node_label in QA_IDS:
    for n in d['flowData']['nodes']:
        if nid not in n['id']:
            continue

        output_lines.append(f'\n### {node_label} ###\n')

        # 1. 检查所有 outputs 字段描述
        np = n['data']['nodeParam']
        for o in n['data']['outputs']:
            fname = o['name']
            desc = o['schema'].get('description', '')
            issues = check_field_desc(desc, fname, node_label)
            if issues:
                for iss in issues:
                    output_lines.append(f'  ❌ [{fname}] {iss}\n')
                    all_issues.append(f'{node_label}#{fname}: {iss}')
            else:
                output_lines.append(f'  ✅ [{fname}] {desc[:80]}\n')

        # 2. 检查 question 文本
        q = np.get('question', '')
        output_lines.append(f'\n  question 工具格式部分:\n')
        idx = q.find('**2. 工具和技能')
        if idx != -1:
            tool_section = q[idx:idx+300]
            output_lines.append(f'    {tool_section}\n')
            # 检查工具部分是否过于严格
            tool_issues = []
            if '如 word / Python' in q:
                tool_issues.append('仍含 "如 word / Python"')
            if '[岗位相关工具' in q:
                tool_issues.append('仍含占位符 "[岗位相关工具"')
            if 'SQL、Python、Tableau' in q:
                tool_issues.append('仍含 "SQL、Python、Tableau"')
            for ti in tool_issues:
                output_lines.append(f'    ❌ {ti}\n')
                all_issues.append(f'{node_label} question: {ti}')

        # 3. 检查整个 question 中是否有危险的精准匹配要求
        danger_patterns = [
            ('如"SQL、Python、Tableau"等', '硬编码 SQL/Python/Tab'),
            ('如 word / Python / Excel', '硬编码 Word/Python/Excel'),
            ('如"暂无"或具体描述', '追问强制格式'),
            ('请补充你掌握的与目标岗位', '追问强制工具格式'),
            ('请补充你描述的实习', '追问强制实习格式'),
            ('[岗位相关工具', '残留占位符'),
            ('[公司/学校]', '残留格式占位符'),
        ]
        for pat, note in danger_patterns:
            if pat in q:
                output_lines.append(f'  ❌ [危险] {note}: "{pat}"\n')
                all_issues.append(f'{node_label} question: {note}')

print('\n' + '=' * 70)
print('扫描结果汇总')
print('=' * 70)

if all_issues:
    print(f'\n❌ 发现 {len(all_issues)} 个风险项:\n')
    for iss in all_issues:
        print(f'  • {iss}')
else:
    print('\n✅ 未发现精准格式匹配风险')

# 打印完整报告
print('\n' + '=' * 70)
print('详细报告')
print('=' * 70)
for line in output_lines:
    print(line, end='')