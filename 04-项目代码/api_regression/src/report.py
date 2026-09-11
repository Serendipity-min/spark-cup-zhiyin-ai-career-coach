"""
Report generator for regression test results (Markdown, CSV, JSON).
Calculates all statistics dynamically from real case execution results.
Distinguishes between VALID PASS, FAIL, WARN, and UNSUPPORTED (UNSUPPORTED not counted as PASS).
Uses standard library exclusively (zero extra numerical dependencies).
"""

import os
import csv
import json
import math
from typing import List, Dict, Any


def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calculates percentile from a list of floats using standard linear interpolation.
    """
    if not values:
        return 0.0
    sorted_v = sorted(values)
    k = (len(sorted_v) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_v[int(k)])
    d0 = sorted_v[int(f)] * (c - k)
    d1 = sorted_v[int(c)] * (k - f)
    return float(d0 + d1)


def generate_reports(case_results: List[Dict[str, Any]], output_dir: str):
    """
    Generates summary.json, summary.csv, and latest_report.md.
    """
    os.makedirs(output_dir, exist_ok=True)

    total_cases = len(case_results)
    valid_pass_count = sum(1 for c in case_results if c.get("status") == "PASS")
    unsupported_count = sum(1 for c in case_results if c.get("status") == "UNSUPPORTED")
    fail_count = sum(1 for c in case_results if c.get("status") == "FAIL")
    warn_count = sum(1 for c in case_results if c.get("status") == "WARN")

    wall_times = [c.get("total_wall_ms", 0) for c in case_results if c.get("total_wall_ms", 0) > 0]
    final_gen_times = [c.get("final_generation_ms", 0) for c in case_results if c.get("final_generation_ms", 0) > 0]
    total_tokens_list = [c.get("total_tokens", 0) for c in case_results if c.get("total_tokens", 0) > 0]

    p50_time = calculate_percentile(wall_times, 50)
    p95_time = calculate_percentile(wall_times, 95)
    avg_time = sum(wall_times) / len(wall_times) if wall_times else 0.0
    max_time = max(wall_times) if wall_times else 0.0
    avg_tokens = sum(total_tokens_list) / len(total_tokens_list) if total_tokens_list else 0.0

    p50_final_gen = calculate_percentile(final_gen_times, 50)
    avg_final_gen = sum(final_gen_times) / len(final_gen_times) if final_gen_times else 0.0

    # Dynamic quality metrics computation
    total_chapter_checks = sum(len(c.get("chapter_checks", {})) for c in case_results)
    passed_chapter_checks = sum(
        sum(1 for v in c.get("chapter_checks", {}).values() if v) for c in case_results
    )
    chapter_pass_rate = (passed_chapter_checks / total_chapter_checks * 100) if total_chapter_checks else 0.0

    total_unrendered_vars = sum(c.get("unrendered_vars_count", 0) for c in case_results)
    job_fidelity_pass_count = sum(1 for c in case_results if c.get("job_fidelity_pass", False))
    job_fidelity_rate = (job_fidelity_pass_count / total_cases * 100) if total_cases else 0.0

    # P0 / P1 / P2 violations
    p0_violations = 0
    p1_violations = 0
    p2_violations = 0

    for c in case_results:
        err_str = " ".join(c.get("errors", []))
        if c.get("status") == "UNSUPPORTED":
            continue
        if not c.get("job_fidelity_pass", True) or "API Error" in err_str or "premature" in err_str:
            p0_violations += 1
        elif c.get("status") == "FAIL":
            p1_violations += 1
        elif c.get("status") == "WARN":
            p2_violations += 1

    # Standardize raw_log to relative path in summary
    for c in case_results:
        if "raw_log" in c and c["raw_log"]:
            c["raw_log"] = os.path.relpath(c["raw_log"], start=output_dir).replace("\\", "/")

    summary_data = {
        "total_cases": total_cases,
        "valid_pass_count": valid_pass_count,
        "pass_count": valid_pass_count,
        "unsupported_count": unsupported_count,
        "fail_count": fail_count,
        "warn_count": warn_count,
        "pass_rate": f"{(valid_pass_count / total_cases * 100):.1f}%" if total_cases else "0%",
        "performance": {
            "p50_ms": round(p50_time, 1),
            "p95_ms": round(p95_time, 1),
            "avg_wall_ms": round(avg_time, 1),
            "max_wall_ms": round(max_time, 1),
            "p50_final_generation_ms": round(p50_final_gen, 1),
            "avg_final_generation_ms": round(avg_final_gen, 1),
            "avg_tokens": round(avg_tokens, 1),
        },
        "quality_metrics": {
            "chapter_pass_rate": f"{chapter_pass_rate:.1f}%",
            "total_unrendered_vars": total_unrendered_vars,
            "job_fidelity_pass_count": job_fidelity_pass_count,
            "job_fidelity_rate": f"{job_fidelity_rate:.1f}%",
            "p0_violations": p0_violations,
            "p1_violations": p1_violations,
            "p2_violations": p2_violations,
        },
        "cases": case_results,
    }

    # 1. JSON Report
    json_path = os.path.join(output_dir, "summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    # 2. CSV Report
    csv_path = os.path.join(output_dir, "summary.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Case ID",
            "Name",
            "Target Job",
            "Status",
            "Interrupt Rounds",
            "Total Wall Time (s)",
            "Final Gen Time (s)",
            "Total Tokens",
            "Ping Count",
            "Char Count",
            "Job Fidelity",
            "Unrendered Vars",
            "Errors",
            "Warnings",
            "Raw Log",
        ])
        for c in case_results:
            writer.writerow([
                c.get("id"),
                c.get("name"),
                c.get("target_job"),
                c.get("status"),
                c.get("interrupt_rounds", 0),
                f"{c.get('total_wall_ms', 0) / 1000.0:.2f}",
                f"{c.get('final_generation_ms', 0) / 1000.0:.2f}",
                c.get("total_tokens", 0),
                c.get("ping_count", 0),
                c.get("char_count", 0),
                "PASS" if c.get("job_fidelity_pass", False) else ("N/A" if c.get("status") == "UNSUPPORTED" else "FAIL"),
                c.get("unrendered_vars_count", 0),
                " | ".join(c.get("errors", [])),
                " | ".join(c.get("warnings", [])),
                c.get("raw_log", ""),
            ])

    # 3. Markdown Report
    md_path = os.path.join(output_dir, "latest_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 职引 · AI职业诊断官 API 批量回归测试报告 (Final)\n\n")
        f.write(f"> 测试模式: 串行执行 (Concurrency = 1)  \n")
        f.write(f"> 总体结论: **有效通过 {valid_pass_count}/{total_cases} (通过率 {summary_data['pass_rate']}) | 平台不支持 {unsupported_count} | 失败 {fail_count}**  \n\n")

        f.write("## 1. 核心性能与指标概览\n\n")
        f.write("| 指标项 | 统计值 |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| **总执行案例数** | {total_cases} |\n")
        f.write(f"| **有效通过 (VALID PASS)** | {valid_pass_count} |\n")
        f.write(f"| **平台不支持 (UNSUPPORTED)** | {unsupported_count} |\n")
        f.write(f"| **告警 (WARN)** | {warn_count} |\n")
        f.write(f"| **失败 (FAIL)** | {fail_count} |\n")
        f.write(f"| **P50 响应耗时** | {p50_time / 1000.0:.2f} s ({p50_time:.0f} ms) |\n")
        f.write(f"| **P95 响应耗时** | {p95_time / 1000.0:.2f} s ({p95_time:.0f} ms) |\n")
        f.write(f"| **平均端到端耗时** | {avg_time / 1000.0:.2f} s |\n")
        f.write(f"| **平均最终生成耗时 (final_generation_ms)** | {avg_final_gen / 1000.0:.2f} s |\n")
        f.write(f"| **单次最大耗时** | {max_time / 1000.0:.2f} s |\n")
        f.write(f"| **平均消耗 Token** | {avg_tokens:.1f} |\n\n")

        f.write("## 2. 逐案例详细执行结果\n\n")
        f.write("| Case ID | 案例名称 | 目标岗位 | 状态 | 中断轮次 | 端到端(s) | 最终生成(s) | Tokens | 结论与备注 |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        for c in case_results:
            st = c.get("status")
            if st == "PASS":
                status_badge = "✅ VALID PASS"
            elif st == "UNSUPPORTED":
                status_badge = "⏸️ UNSUPPORTED"
            elif st == "WARN":
                status_badge = "⚠️ WARN"
            else:
                status_badge = "❌ FAIL"

            wall_s = f"{c.get('total_wall_ms', 0) / 1000.0:.1f}s"
            gen_s = f"{c.get('final_generation_ms', 0) / 1000.0:.1f}s"
            notes = " | ".join(c.get("errors", []) + c.get("warnings", []))
            if not notes:
                notes = "全指标符合规范"
            f.write(f"| `{c.get('id')}` | {c.get('name')} | `{c.get('target_job')}` | {status_badge} | {c.get('interrupt_rounds')} | {wall_s} | {gen_s} | {c.get('total_tokens')} | {notes} |\n")

        f.write("\n## 3. 质量门禁与专项分析（真实数据动态统计）\n\n")
        f.write(f"- **六大必含章节通过率**: {chapter_pass_rate:.1f}% ({passed_chapter_checks}/{total_chapter_checks} 项检查通过)\n")
        f.write(f"- **岗位保真通过率**: {job_fidelity_rate:.1f}% ({job_fidelity_pass_count}/{total_cases} 个案例保真)\n")
        f.write(f"- **模板未渲染变量残留**: 共发现 {total_unrendered_vars} 例 `{{{{xxx}}}}` 变量残留\n")
        f.write(f"- **P0 严重阻断级缺陷**: {p0_violations} 项\n")
        f.write(f"- **P1 主要功能级缺陷**: {p1_violations} 项\n")
        f.write(f"- **P2 格式告警级缺陷**: {p2_violations} 项\n\n")

        f.write("## 4. 建议与发布结论\n\n")
        if fail_count == 0 and p0_violations == 0:
            f.write("> 🏆 **结论: 建议冻结为复赛 Final 版本！**\n>\n> 工作流 API 接口稳定性、多轮问答状态机恢复能力、报告内容规范性与岗位保真度全部达标，可直接作为复赛提交与演示的基准版本。\n")
        else:
            f.write(f"> ❌ **结论: 未通过 Final Gate（存在 {fail_count} 个失败案例，{p0_violations} 个 P0 阻断项），不建议冻结。**\n")

    return summary_data
