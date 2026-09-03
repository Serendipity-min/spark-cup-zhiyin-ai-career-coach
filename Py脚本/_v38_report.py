# -*- coding: utf-8 -*-
"""v3.8 输出报告"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

src = r'E:\workbuddy_projrct\星火杯\职引_v3.7.yml'
dst = r'E:\workbuddy_projrct\星火杯\职引_v3.8_精确可视化.yml'

with open(dst, encoding='utf-8') as f:
    t = f.read()

print("=" * 70)
print(" V3.8 修复版 生成报告")
print("=" * 70)
print()
print(f"  输入文件: {src}")
print(f"  输出文件: {dst}")
print(f"  输出大小: {os.path.getsize(dst) / 1024:.1f} KB  ({len(t):,} 字符)")
print(f"  较 v3.7: {os.path.getsize(dst) - os.path.getsize(src):+,} 字节")
print()

# 10 项关键校验
checks = [
    ("1. 规则 0 整体重写（精确规范 + 对照表 + 自检）", "规则 0：可视化精确规范" in t and "对照表" in t),
    ("2. 核心原则双重约束（长度+方块数）", "长度固定 + 方块数精确" in t),
    ("3. 二节20格对照表（20行）", "20 格" in t and "评分 1.0 → ■×2" in t),
    ("4. 七节10格对照表（20行）", "分数 0.5 → ■×1" in t and "分数 10.0 → ■×10" in t),
    ("5. 周进度条对照表（10格，禁止12格）", "禁止12格" in t and "P0-P3" in t),
    ("6. 自检清单（输出前逐条核对）", "自检清单" in t and "输出前必须" in t),
    ("7. 二节规则强化（强制查表）", "二节可视化规则" in t and "查上方对照表" in t),
    ("8. 四节规则强化（强制10格）", "严格10格" in t),
    ("9. 六节综合能力10格强化", "综合能力可视化：**10格精确条" in t),
    ("10. user template 追加可视化警告", "严格可视化规范警告" in t),
]

passed = 0
for desc, ok in checks:
    flag = "[OK]" if ok else "[FAIL]"
    print(f"  {flag} {desc}")
    if ok:
        passed += 1

print()
print(f"  校验通过: {passed}/10")
print()

# 提示对比 v3.7 的具体差异
print("=" * 70)
print(" 主要修复内容（差异点）")
print("=" * 70)

print("""
  【规则 0 完全重写】
    v3.7: 模糊规则 "长度规范" + 示例（仅给 3 个例子）
    v3.8: 强制规范 + 6 类用途长度表 + 评分↔方块对照表（二节20行/七节20行/四节5行）
          + 5 章精确示例 + 自检清单

  【二节规则】
    v3.7: "int(round(评分 / 10 * 20)) 个 ■，剩余用 □"
    v3.8: "禁止使用任何其他计算方式，不要自己算" + "写条之前先查上方对照表，然后照抄对应行"

  【四节周进度】
    v3.7: 示例用 12 格 `[━━━━━━──────]`（LLM 误认为可这样写）
    v3.8: 明确 "禁止写12格的进度条！12格是错误的，只写10格！"
          + 5 行精确对照表

  【七节成长路径】
    v3.7: 模板示例全是 20 格（LLM 全部照抄错位）
    v3.8: 模板示例改为 10 格 + 强制■数 = round(评分)

  【六节综合能力】
    v3.7: 模糊 "评分个 ■" + (10-评分) 个 □"（LLM 自由发挥）
    v3.8: "10格精确条，■数 = round(综合分)" + 3 个严格示例

  【新增：自检清单】
    6 项必须逐条核对（长度、■数、对照表查询）

  【新增：user 模板警告】
    在用户输入位置追加可视化强提醒，要求 LLM 写完后核对
""")

print("=" * 70)
print(" 下一步")
print("=" * 70)
print("""
  1. 把 职引_v3.8_精确可视化.yml 导入星火平台，发布新版本
  2. 重新跑 V3.7test 那 14 个样本，记录为 V3.8test
  3. 用 _audit_v37_v2.py 校验 V3.8test 结果（应大幅减少问题）
""")
