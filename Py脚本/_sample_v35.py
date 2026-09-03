# -*- coding: utf-8 -*-
"""
模拟 LLM 接到新 prompt 后会生成的样例报告片段
（用 Python 模拟可视化生成逻辑）
"""

def make_bar(score, width=20):
    """生成 N 格进度条"""
    filled = round(score / 10 * width)
    return '[' + '#' * filled + '-' * (width - filled) + ']'

def make_gap(gap, width=10):
    """生成差距柱"""
    if gap <= 0:
        return '[已达标]'
    return '[' + '+' * gap + '-' * (width - gap) + ']'

def make_week_progress(week_num):
    """生成第 N 周进度条"""
    filled = week_num * 2
    return '[' + '#' * filled + '.' * (10 - filled) + ']'

# ============================================================
# 模拟输出报告（数据运营助理 / 大一 数据科学）
# ============================================================
print('# 数据运营助理 能力诊断报告')
print()

print('## 二、能力现状评估')
print()
print('| 能力维度 | 当前水平 | 评分 | 可视化 | 评估依据 |')
print('|---------|---------|------|--------|---------|')
evals = [
    ('数据分析与工具应用', '理论入门', 2.0, '"Excel/Python词云/校内勤工俭学，但暂无系统项目"'),
    ('业务理解与指标拆解', '几乎空白', 1.0, '"暂无任何商业场景经历"'),
    ('SQL 数据查询', '未开始', 1.0, '"未提及"'),
    ('数据可视化', '未开始', 1.0, '"未提及"'),
    ('办公软件（Excel）', '基础水平', 4.0, '"Excel 有基础操作"'),
    ('沟通协作', '潜力期', 4.0, '"勤工俭学体现基础协作"'),
    ('学习能力', '在校生', 5.5, '"大一时已开始思考职业"'),
]
for dim, level, score, basis in evals:
    bar = make_bar(score)
    print(f'| {dim} | {level} | {score}/10 | `{bar}` | {basis} |')
print()

print('## 三、关键差距分析 TOP3')
print()
print('| 差距描述 | 现状 vs 要求 | 真实场景影响 |')
print('|---------|-------------|-------------|')
gaps_top3 = [
    ('核心技能零实践', '你"工具暂无" vs 岗位要求熟练 Python+SQL', '简历筛选无关键词，面试无技术可聊'),
    ('商业认知空白', '你"暂无业务经历" vs 岗位要求业务理解', '无法回答"为什么分析"这类核心问题'),
    ('项目经验缺失', '你"暂无项目" vs 竞争者有 1-2 段经历', '同等技术下简历无亮点'),
]
for g in gaps_top3:
    print(f'| {g[0]} | {g[1]} | {g[2]} |')
print()

print('**差距可视化表：**')
print()
print('| 能力维度 | 你的水平 | 岗位要求 | 差距 | 差距可视化 |')
print('|---------|---------|---------|------|-----------|')
gap_data = [
    ('SQL', 1, 9, 8),
    ('Python 数据分析', 2, 8, 6),
    ('业务理解', 1, 9, 8),
]
for dim, mine, need, gap in gap_data:
    bar = make_gap(gap)
    print(f'| {dim} | {mine}/10 | {need}/10 | {gap} | `{bar}` |')
print()

print('## 四、补齐方案：4 周行动表')
print()
print('| 优先级 | 具体任务 | 推荐资源 | 衡量标准 | 周进度可视化 |')
print('|--------|---------|---------|---------|-------------|')
plan = [
    ('P0', '掌握 Python + SQL 核心语法', '廖雪峰Python / LeetCode SQL', '能完成 10 道 SQL 简单题', '[####] 4周连续'),
    ('P1', '用 Excel 做一次业务数据分析', 'B站王佩丰Excel / GrowingIO博客', '能解释DAU/留存等核心指标', '[..##..] W2-W3'),
    ('P2', '完成一个端到端的分析项目', 'Kaggle数据集 / 和鲸社区', '产出 1 份 Jupyter Notebook', '[...#.] W3-W4'),
    ('P3', '启动信息搜集 + networking', '实习僧 / 牛客网 / 学长学姐', '整理 5 个目标岗位 JD', '[...#.] W4'),
]
for p in plan:
    print(f'| {p[0]} | {p[1]} | {p[2]} | {p[3]} | `{p[4]}` |')
print()

print('## 四·补、四周行动时间线总览')
print()
print('| 周次 | 重点任务 | 完成进度 |')
print('|------|---------|---------|')
weeks = [
    (1, '掌握 Python + SQL 核心语法', make_week_progress(1)),
    (2, 'Excel 强化 + 学习业务指标', make_week_progress(2)),
    (3, '完成数据分析小项目', make_week_progress(3)),
    (4, '投递实习 + 模拟面试', make_week_progress(4)),
]
for w in weeks:
    print(f'| 第{w[0]}周 | {w[1]} | `{w[2]}` |')
print()

print('## 六、整体评分与寄语')
print()
print('- 综合能力评分：2.1/10')
print(f'- 综合能力可视化：`{make_bar(2.1, 10)}`')
print('- 校招竞争力评级：C（一般）')
print('- 鼓励性寄语：大一是黄金规划期，把这张白纸变成绚丽画卷。')
print()

print('## 七、能力成长路径图')
print()
print('现在：')
print('```')
print('  SQL | Python | 业务 | 沟通 | 学习')
print('   1  |   2    |  1   |  4   |  5.5')
print('```')
print()
print('4 周后：')
print('```')
print('  SQL | Python | 业务 | 沟通 | 学习')
print('   6  |   7    |  5   |  6   |  7')
print('```')
print()

print('=' * 60)
print('样例生成完成！所有可视化已嵌入报告。')
print('=' * 60)