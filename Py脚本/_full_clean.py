# -*- coding: utf-8 -*-
"""
全面清理所有占位符 + 简化格式参考
修复项：
  1. QA3 question 格式参考中的所有 [占位符] → 改为自然语言描述
  2. QA3 question 工具行格式 → 进一步通用化
  3. QA2 question 工具提示示例（word/Python/Excel）→ 通用化
"""
import yaml, sys
sys.stdout.reconfigure(encoding='utf-8')

fn = r'E:\workbuddy_projrct\星火杯\职引_v3.3_死循环修复.yml'
with open(fn, 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

def find_node(prefix):
    for n in d['flowData']['nodes']:
        if n['id'].startswith(prefix):
            return n
    return None

print('=== 开始全面清理 ===\n')

# ============================================================
# 修复 1：QA3 question — 清理所有格式占位符
# ============================================================
QA3 = find_node('question-answer::3f928444')
if QA3:
    old_q = QA3['data']['nodeParam']['question']

    # 原来格式参考（含占位符）：
    # **1. 实习/项目经历**（选最重要的 1-2 段）：
    # - 在 [公司/学校] 做了 [什么岗位/项目]
    # - 主要负责 [具体工作]
    # - 取得了 [量化结果]（如 DAU 提升 12%、节省 50% 时间等）

    old_format = """**1. 实习/项目经历**（选最重要的 1-2 段）：
- 在 [公司/学校] 做了 [什么岗位/项目]
- 主要负责 [具体工作]
- 取得了 [量化结果]（如 DAU 提升 12%、节省 50% 时间等）"""

    new_format = """**1. 实习/项目经历**（选最重要的 1-2 段）：
- 在什么公司或学校，做了什么岗位或项目
- 主要负责什么工作
- 取得了什么结果（尽量量化，比如：用户增长10%、效率提升30%等）

💡 没有实习也没关系，告诉我你做过的课程项目、校园活动或个人作品，一样有用！"""

    if old_format in old_q:
        new_q = old_q.replace(old_format, new_format)
        print('✅ QA3: 清理格式占位符（精确匹配）')
    else:
        # 模糊替换
        replacements = [
            ('[公司/学校]', '什么公司或学校'),
            ('[什么岗位/项目]', '什么岗位或项目'),
            ('[具体工作]', '主要负责什么'),
            ('[量化结果]', '取得了什么结果'),
            ('如 DAU 提升 12%、节省 50% 时间等', '尽量量化，比如：用户增长10%、效率提升30%'),
        ]
        new_q = old_q
        for old, new in replacements:
            if old in new_q:
                new_q = new_q.replace(old, new)
                print(f'✅ QA3: 替换 "{old[:20]}..."')

    # 工具格式进一步通用化（去掉具体工具示例）
    # 现在是：**2. 工具和技能**（有哪些就列哪些，如：Excel、Python、PS等；如果暂时没有，直接写"暂无"即可）：
    # 改为：**2. 工具和技能**（有哪些就列哪些，不会就写"暂无"）：
    old_tools = '**2. 工具和技能**（有哪些就列哪些，如：Excel、Python、PS等；如果暂时没有，直接写"暂无"即可）：'
    new_tools = '**2. 工具和技能**（有哪些就列哪些，实在没有就写"暂无"）：'
    if old_tools in new_q:
        new_q = new_q.replace(old_tools, new_tools)
        print('✅ QA3: 工具提示进一步通用化')

    if new_q != old_q:
        QA3['data']['nodeParam']['question'] = new_q
        print(f'✅ QA3: question 已更新\n')

# ============================================================
# 修复 2：QA2 question — 工具示例行通用化
# QA2 没有问工具，所以不用动
# ============================================================
print('QA2: 无需修改（不询问工具）')

# ============================================================
# 修复 3：QA3 skills 字段描述 — 确保完全不要求格式
# ============================================================
for o in QA3['data']['outputs']:
    if o['name'] == 'skills':
        old_desc = o['schema']['description']
        # 当前已经是"直接转述"，确认一下
        if '直接转述' in old_desc and '无需标准化' in old_desc:
            print(f'✅ QA3 skills 字段: 已是安全描述，无需修改')
        else:
            new_desc = '用户自述掌握的与目标岗位相关的工具或技能，直接转述用户原话即可，无需标准化。如果用户说"暂无"或"无"或任何表示没有的回答，填"暂无"。'
            o['schema']['description'] = new_desc
            print(f'✅ QA3 skills 字段: 已更新')

# ============================================================
# 保存
# ============================================================
with open(fn, 'w', encoding='utf-8') as f:
    yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
print(f'\n✅ 已保存: {fn}')

# ============================================================
# 最终验证
# ============================================================
print('\n=== 最终验证 ===\n')

with open(fn, encoding='utf-8') as f:
    final = yaml.safe_load(f)

checks_all = [
    '[公司/学校]', '[什么岗位/项目]', '[具体工作]', '[量化结果]',
    'SQL、Python、Tableau', 'word / Python / Excel', 'word / Python /',
    'Figma', 'Tableau',
    '如"暂无"或具体描述',
    '请补充你掌握的与目标岗位',
    '请补充你描述的实习',
    '[岗位相关工具',
]

for nid, label in [('c17e1d8f', 'QA1'), ('8b7f2f5a', 'QA2'), ('3f928444', 'QA3')]:
    for n in final['flowData']['nodes']:
        if nid in n['id']:
            q = n['data']['nodeParam'].get('question', '')
            # 检查字段描述
            for o in n['data']['outputs']:
                dsc = o['schema'].get('description', '')
                q += dsc

            issues = [kw for kw in checks_all if kw in q]
            if issues:
                print(f'  ❌ {label}: 发现 {len(issues)} 个风险词: {issues}')
            else:
                print(f'  ✅ {label}: 完全干净')

# 打印最终 QA3 question 完整内容
print('\n=== QA3 完整 question（供人工确认）===\n')
for n in final['flowData']['nodes']:
    if '3f928444' in n['id']:
        print(n['data']['nodeParam']['question'])
        break

print('\n✅ 全部检查完成')