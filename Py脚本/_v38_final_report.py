# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

dst = r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml'
src = r'E:\workbuddy_projrct\星火杯\职引_v3.7.yml'

with open(dst, encoding='utf-8') as f:
    t = f.read()

print('=' * 70)
print(' V3.8 精确可视化版 - 最终生成报告')
print('=' * 70)
print()
print(f'  源文件: {src}')
print(f'  目标:   {dst}')
print(f'  大小:   {os.path.getsize(dst) / 1024:.1f} KB ({len(t):,} 字符)')
print(f'  较 v3.7: {len(t) - os.path.getsize(src):+,} 字节')
print()

# 10 项关键校验
checks = [
    ("1. 规则 0 完全重写（精确规范+对照表+自检）", "规则 0：可视化精确规范" in t and "二节专用对照表" in t),
    ("2. P0-P3 禁止 12 格警告", "禁止12格" in t and "P0-P3对照表" in t),
    ("3. 自检清单 6 项核对项", "自检清单（输出前必须逐条核对）" in t and "■ 数是否 = round(评分×2)" in t),
    ("4. 二节强制查对照表", "禁止自己算" in t and "查规则0中的" in t),
    ("5. 四节严格 10 格", "严格10格，禁止12格" in t),
    ("6. 六节 10 格精确条", "10格精确条" in t and "长度不是10格" in t),
    ("7. 七节 10 格模板（[■■□□□□□□□]）", "[■■□□□□□□□]" in t),
    ("8. 七节 10 格模板（[■■■■□□□□□]）", "[■■■■□□□□□]" in t),
    ("9. user 模板警告（v3.8标记）", "【v3.8可视化强化提醒】" in t),
    ("10. 三节严格 10 格", "严格10格，不允许偏差" in t and "round(差距)" in t),
    ("11. 七节表格说明（10格严格）", "10格，严格精确" in t),
    ("12. 规则0长度规范表", "| 二、能力现状评估 | 能力评分条 | **20 格**" in t),
    ("13. 规则0评分对照表", "评分 1.0 → ■×2" in t and "评分 10.0 → ■×20" in t),
    ("14. 规则0周进度对照表", "P0 全周期(4周)" in t and "P3 最后1周" in t),
]

passed = 0
for desc, ok in checks:
    print(f'  {"[OK]" if ok else "[FAIL]"} {desc}')
    if ok: passed += 1

print()
print(f'  校验通过: {passed}/{len(checks)}')
print()

# 文件统计
import re
sysTpl_match = re.search(r'systemTemplate:\s*"([^"]+)"', t)
if sysTpl_match:
    print(f'  systemTemplate 长度: {len(sysTpl_match.group(1)):,} 字符')

print()
print('=' * 70)
print(' 主要修复内容（差异点）')
print('=' * 70)

print('''
  【规则 0 完全重写】
    v3.7: 模糊规则 + 4 个示例
    v3.8: 强制规范 + 6 类用途长度表 + 3 张精确对照表（二节20行 / 七节20行 / 四节P0-P3 4行）
          + 5 章精确示例 + 6 项自检清单

  【二节规则】
    v3.7: "int(round(评分 / 10 * 20)) 个 ■，剩余用 □"
    v3.8: "禁止自己算" + "查规则0中的二节专用对照表，照抄对应行"

  【四节周进度】
    v3.7: 示例用 12 格（LLM 误以为可这样写）
    v3.8: 明确 "禁止12格！12格是错误的" + 4 行精确对照表

  【七节成长路径模板】
    v3.7: 模板示例全是 20 格（LLM 全部照抄）
    v3.8: 模板示例改为 10 格 + 强制■数 = round(评分)

  【六节综合能力】
    v3.7: "[评分个 ■ + (10-评分) 个 □]"
    v3.8: "10格精确条，■数 = round(综合分)" + 严格示例

  【新增：自检清单】
    6 项必须逐条核对（长度、■数、对照表查询）

  【新增：user 模板警告】
    在用户输入位置追加【v3.8可视化强化提醒】
''')

print('=' * 70)
print(' 下一步操作')
print('=' * 70)
print('''
  1. 在星火平台创建新工作流，导入 职引_v3.8_精确可视化.yml
  2. 发布新版本（建议命名为 v3.8-精确可视化版）
  3. 用 V3.7test 的 14 个样本重新测试，记录为 V3.8test
  4. 用 _audit_v37_v2.py 校验（应大幅减少甚至消灭问题）
  5. 如果问题归零，可作为终版提交

  提示：
  - systemTemplate 长度 6,393 字符（v3.7 是 4,409）
  - maxTokens 12288 / temperature 0.5（v5 优化保留）
  - 模型 DeepSeek-V3.1
''')
