"""
Assertion logic and quality checks for Xingchen Career Diagnosis Reports.
Strictly evaluates the final generated report text (isolated from dialog transcript).
"""

import re
from typing import Dict, Any, List, Optional


REQUIRED_CHAPTERS = [
    "岗位核心能力拆解",
    "能力现状评估",
    "关键差距分析",
    "行动计划",
    "面试准备建议",
    "整体评分",
]

REQUIRED_DIMENSIONS = [
    "综合能力评分",
    "校招准备度评级",
    "诊断可信度",
    "证据覆盖度",
]


def evaluate_report(
    final_text: str,
    target_job: str,
    case_expectations: Dict[str, Any],
    interrupt_questions: List[str],
) -> Dict[str, Any]:
    """
    Evaluates final output text against the contract quality standards.
    """
    results = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "chapter_checks": {},
        "dimension_checks": {},
        "char_count": len(final_text),
        "unrendered_vars_count": 0,
        "unrendered_vars": [],
        "forbidden_matches": [],
        "job_fidelity_pass": True,
    }

    # 1. Non-empty check
    if not final_text.strip():
        results["passed"] = False
        results["errors"].append("Final report text is completely empty.")
        return results

    # 2. Length check (>= 500 hard fail, < 1000 warning)
    if len(final_text) < 500:
        results["passed"] = False
        results["errors"].append(f"Report too short ({len(final_text)} chars < 500 threshold).")
    elif len(final_text) < 1000:
        results["warnings"].append(f"Report length ({len(final_text)} chars) is below recommended 1000 chars.")

    # 3. Unrendered variable check (e.g. {{xxx}})
    unrendered = re.findall(r"\{\{[^}]+\}\}", final_text)
    results["unrendered_vars_count"] = len(unrendered)
    if unrendered:
        results["passed"] = False
        results["unrendered_vars"] = unrendered
        results["errors"].append(f"Found unrendered template variables: {unrendered}")

    # 4. Required chapters check (on final report text)
    for chapter in REQUIRED_CHAPTERS:
        present = chapter in final_text
        if not present and chapter == "行动计划":
            present = bool(re.search(r"[0-9四]周行动计划", final_text))
        results["chapter_checks"][chapter] = present
        if not present:
            results["passed"] = False
            results["errors"].append(f"Missing required chapter in final report: '{chapter}'")

    # 5. Required dimensions check
    for dim in REQUIRED_DIMENSIONS:
        present = dim in final_text
        results["dimension_checks"][dim] = present
        if not present:
            results["warnings"].append(f"Missing dimension keyword: '{dim}'")

    # 6. Target job fidelity check on final report text
    if target_job:
        job_core = target_job.replace("工程师", "").replace("岗位", "").strip()
        if job_core not in final_text:
            results["passed"] = False
            results["job_fidelity_pass"] = False
            results["errors"].append(f"Target job core '{job_core}' not found in final report text.")

    # 7. Forbidden keywords check
    forbidden_list = case_expectations.get("forbidden", [])
    for forb in forbidden_list:
        if forb in final_text:
            results["passed"] = False
            results["forbidden_matches"].append(forb)
            results["job_fidelity_pass"] = False
            results["errors"].append(f"Found forbidden keyword '{forb}' in final report.")

    # 8. expectations.final_contains check (HARD FAIL if missing)
    final_contains_list = case_expectations.get("final_contains", [])
    for req_item in final_contains_list:
        if req_item not in final_text:
            results["passed"] = False
            results["errors"].append(f"Required keyword '{req_item}' not found in final report.")

    # 9. expectations.first_interrupt_contains check (HARD FAIL if mismatch)
    first_int_exp = case_expectations.get("first_interrupt_contains")
    if first_int_exp:
        if not interrupt_questions:
            results["passed"] = False
            results["errors"].append(f"Expected first interrupt containing '{first_int_exp}', but got 0 interrupts.")
        else:
            first_q = interrupt_questions[0]
            if first_int_exp not in first_q:
                results["passed"] = False
                results["errors"].append(
                    f"First interrupt question '{first_q[:50]}...' did not contain expected keyword '{first_int_exp}'."
                )

    # 10. expectations.expected_interrupt_rounds (HARD FAIL if mismatch)
    exp_rounds = case_expectations.get("expected_interrupt_rounds")
    if exp_rounds is not None:
        if len(interrupt_questions) != exp_rounds:
            results["passed"] = False
            results["errors"].append(
                f"Expected exactly {exp_rounds} interrupt rounds, but observed {len(interrupt_questions)} rounds."
            )

    return results
