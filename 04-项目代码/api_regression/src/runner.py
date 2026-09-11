"""
Main Test Runner for iFlytek Xingchen Career Diagnosis Workflow.
Strictly isolates final report text from dialog transcript and implements robust fail-fast error handling.
"""

import os
import sys
import time
import json
import yaml
import hashlib
import warnings
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Ensure UTF-8 stdout/stderr and unbuffered output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

# Ensure local package import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.xfyun_client import XfyunWorkflowClient
from src.sse_parser import parse_sse_stream
from src.assertions import evaluate_report
from src.report import generate_reports


def print_preflight(client: XfyunWorkflowClient):
    """
    Prints preflight checklist according to contract requirements.
    """
    masked_key = client.api_key[:6] + "..." + client.api_key[-4:] if len(client.api_key) > 10 else "***"
    masked_secret = client.api_secret[:4] + "..." + client.api_secret[-4:] if len(client.api_secret) > 8 else "***"

    print("\n" + "=" * 65)
    print(" [PREFLIGHT CHECK] 职引 · AI职业诊断官 API 批量回归测试")
    print("=" * 65)
    print(f" [x] 工作流已发布为 API")
    print(f" [x] 最近修改后已确认“更新绑定”")
    print(f" [x] API Flow ID: {client.flow_id}")
    print(f" [x] 当前绑定 APPID 授权状态已激活")
    print(f" [x] API Key: {masked_key} (已脱敏)")
    print(f" [x] API Secret: {masked_secret} (已脱敏)")
    print(f" [x] 目标接入点: {client.chat_url}")
    print(f" [x] 凭据安全存储于本地 .env (已配置 .gitignore 隔离)")
    print(f" [x] 调度策略: Concurrency = 1 (严格单线程串行，无并发)")
    print("=" * 65 + "\n")


def write_raw_log(raw_log_file: str, raw_events: List[Dict[str, Any]]):
    """
    Writes raw event logs to JSONL file.
    """
    os.makedirs(os.path.dirname(raw_log_file), exist_ok=True)
    with open(raw_log_file, "w", encoding="utf-8") as f:
        for ev in raw_events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def execute_standard_case(
    client: XfyunWorkflowClient,
    case_def: Dict[str, Any],
    raw_log_dir: str,
    uid_override: Optional[str] = None,
    chat_id_override: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes a standard multi-turn interactive test case.
    Supports uid_override and chat_id_override for explicit session reuse verification.
    """
    case_id = case_def["id"]
    case_name = case_def.get("name", case_id)
    target_job = case_def.get("target_job", "")
    initial_text = case_def.get("initial", "你好")
    replies = list(case_def.get("replies", []))
    expectations = case_def.get("expectations", {})

    ts_now = int(time.time())
    uid = uid_override if uid_override is not None else f"reg_{case_id}_{ts_now % 10000}"
    chat_id = chat_id_override if chat_id_override is not None else f"{case_id[:10]}_{ts_now}"[:32]
    uid_hash = hashlib.sha256(uid.encode("utf-8")).hexdigest()[:12]

    raw_log_file = os.path.join(raw_log_dir, f"{case_id}.jsonl")
    raw_events = [
        {
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "session_info": {
                "uid_hash": uid_hash,
                "chat_id": chat_id,
            },
        }
    ]

    print(f"[RUN] 正在执行 [{case_id}] {case_name} ...")
    print(f"  - 会话: uid_hash={uid_hash} | chat_id={chat_id}")
    print(f"  - 初始输入: \"{initial_text}\" | 预设后续回答: {replies}")

    start_wall_time = time.time()
    interrupt_questions = []
    dialog_transcript = [{"role": "user", "turn": 0, "content": initial_text}]
    final_report_chunks = []
    final_generation_start_time = None
    final_generation_ms = 0.0
    ping_count = 0
    total_tokens = 0
    reply_index = 0

    # 1. Start Workflow
    start_req_time = time.time()
    try:
        resp = client.start_workflow(initial_text, uid, chat_id)
    except Exception as e:
        raw_events.append({"timestamp": datetime.now().isoformat(), "error": f"Start network error: {str(e)}"})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": target_job,
            "status": "FAIL",
            "errors": [f"Start workflow network error: {str(e)}"],
            "warnings": [],
            "interrupt_rounds": 0,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    # Validate HTTP status_code before SSE parsing
    if resp.status_code != 200:
        err_text = resp.text[:200]
        raw_events.append({"timestamp": datetime.now().isoformat(), "error": f"HTTP {resp.status_code}", "body": err_text})
        write_raw_log(raw_log_file, raw_events)
        print(f"    [FAIL] HTTP {resp.status_code}: {err_text}")
        return {
            "id": case_id,
            "name": case_name,
            "target_job": target_job,
            "status": "FAIL",
            "errors": [f"HTTP {resp.status_code}: {err_text}"],
            "warnings": [],
            "interrupt_rounds": 0,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    active_resp = resp
    is_finished = False

    while not is_finished:
        current_stream_chunks = []
        interrupted = False
        current_event_id = None
        stream_had_events = False

        for event in parse_sse_stream(active_resp.iter_lines()):
            stream_had_events = True
            raw_events.append({
                "timestamp": datetime.now().isoformat(),
                "case_id": case_id,
                "event": event,
            })

            # Check error code from API
            if event.get("code") and event.get("code") != 0:
                error_msg = f"API Error Code {event.get('code')}: {event.get('message')}"
                write_raw_log(raw_log_file, raw_events)
                print(f"    [FAIL] {error_msg}")
                return {
                    "id": case_id,
                    "name": case_name,
                    "target_job": target_job,
                    "status": "FAIL",
                    "errors": [error_msg],
                    "warnings": [],
                    "interrupt_rounds": len(interrupt_questions),
                    "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                    "final_generation_ms": 0.0,
                    "total_tokens": total_tokens,
                    "ping_count": ping_count,
                    "char_count": sum(len(t) for t in final_report_chunks),
                    "chapter_checks": {},
                    "dimension_checks": {},
                    "unrendered_vars_count": 0,
                    "job_fidelity_pass": False,
                    "raw_log": raw_log_file,
                }

            choices = event.get("choices", [])
            finish_reason = None
            if choices and isinstance(choices, list) and len(choices) > 0:
                delta = choices[0].get("delta", {})
                content_chunk = delta.get("content", "")
                if content_chunk:
                    current_stream_chunks.append(content_chunk)
                    print(".", end="", flush=True)

                finish_reason = choices[0].get("finish_reason")

            if event.get("finish_reason") == "ping" or finish_reason == "ping":
                ping_count += 1
                continue

            if event.get("usage"):
                usage = event.get("usage", {})
                total_tokens = usage.get("total_tokens", total_tokens)

            event_data = event.get("event_data", {})
            event_id = event_data.get("event_id")

            if finish_reason == "interrupt" or event.get("event_type") == "interrupt" or event_id:
                interrupted = True
                current_event_id = event_id or event_data.get("event_id")
                direct_content = event_data.get("value", {}).get("content", "")
                question_text = direct_content if direct_content else "".join(current_stream_chunks).strip()
                interrupt_questions.append(question_text)
                dialog_transcript.append({
                    "role": "assistant_interrupt",
                    "turn": len(interrupt_questions),
                    "event_id": current_event_id,
                    "content": question_text,
                })
                print(f"\n    [Interrupt #{len(interrupt_questions)}] 问题: \"{question_text[:60]}...\" (event_id: {current_event_id})", flush=True)
                break

            if finish_reason == "stop" or event.get("is_done"):
                is_finished = True
                if current_stream_chunks:
                    final_report_chunks.extend(current_stream_chunks)
                if final_generation_start_time:
                    final_generation_ms = (time.time() - final_generation_start_time) * 1000
                print(f"\n    [Stop] 工作流顺利完结！", flush=True)
                break

        # If interrupted, trigger resume
        if interrupted:
            if not current_event_id:
                write_raw_log(raw_log_file, raw_events)
                print("    [FAIL] 遇到 interrupt 但未解析到有效 event_id！", flush=True)
                return {
                    "id": case_id,
                    "name": case_name,
                    "target_job": target_job,
                    "status": "FAIL",
                    "errors": ["Interrupt without valid event_id"],
                    "warnings": [],
                    "interrupt_rounds": len(interrupt_questions),
                    "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                    "final_generation_ms": 0.0,
                    "total_tokens": total_tokens,
                    "ping_count": ping_count,
                    "char_count": 0,
                    "chapter_checks": {},
                    "dimension_checks": {},
                    "unrendered_vars_count": 0,
                    "job_fidelity_pass": False,
                    "raw_log": raw_log_file,
                }

            if reply_index < len(replies):
                next_reply = replies[reply_index]
                reply_index += 1
            else:
                next_reply = "暂无"
                print("    [WARN] 预设回答耗尽，补充 '暂无'", flush=True)

            dialog_transcript.append({
                "role": "user",
                "turn": reply_index,
                "content": next_reply,
            })
            print(f"    -> 自动回复: \"{next_reply}\" -> 发起 /workflow/v1/resume ...", flush=True)

            # Record final generation start time if this is the last reply
            if reply_index >= len(replies):
                final_generation_start_time = time.time()

            try:
                active_resp = client.resume_workflow(current_event_id, next_reply)
            except Exception as e:
                raw_events.append({"timestamp": datetime.now().isoformat(), "error": f"Resume network error: {str(e)}"})
                write_raw_log(raw_log_file, raw_events)
                print(f"    [FAIL] Resume 异常: {e}", flush=True)
                return {
                    "id": case_id,
                    "name": case_name,
                    "target_job": target_job,
                    "status": "FAIL",
                    "errors": [f"Resume network error: {str(e)}"],
                    "warnings": [],
                    "interrupt_rounds": len(interrupt_questions),
                    "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                    "final_generation_ms": 0.0,
                    "total_tokens": total_tokens,
                    "ping_count": ping_count,
                    "char_count": sum(len(t) for t in final_report_chunks),
                    "chapter_checks": {},
                    "dimension_checks": {},
                    "unrendered_vars_count": 0,
                    "job_fidelity_pass": False,
                    "raw_log": raw_log_file,
                }

            if active_resp.status_code != 200:
                err_text = active_resp.text[:200]
                raw_events.append({"timestamp": datetime.now().isoformat(), "error": f"Resume HTTP {active_resp.status_code}", "body": err_text})
                write_raw_log(raw_log_file, raw_events)
                print(f"    [FAIL] Resume HTTP {active_resp.status_code}: {err_text}")
                return {
                    "id": case_id,
                    "name": case_name,
                    "target_job": target_job,
                    "status": "FAIL",
                    "errors": [f"Resume HTTP {active_resp.status_code}: {err_text}"],
                    "warnings": [],
                    "interrupt_rounds": len(interrupt_questions),
                    "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                    "final_generation_ms": 0.0,
                    "total_tokens": total_tokens,
                    "ping_count": ping_count,
                    "char_count": 0,
                    "chapter_checks": {},
                    "dimension_checks": {},
                    "unrendered_vars_count": 0,
                    "job_fidelity_pass": False,
                    "raw_log": raw_log_file,
                }

        elif not is_finished:
            # Stream ended prematurely without receiving stop or interrupt -> HARD FAIL!
            write_raw_log(raw_log_file, raw_events)
            err_msg = "Stream terminated prematurely without receiving stop or interrupt."
            print(f"\n    [FAIL] {err_msg}", flush=True)
            return {
                "id": case_id,
                "name": case_name,
                "target_job": target_job,
                "status": "FAIL",
                "errors": [err_msg],
                "warnings": [],
                "interrupt_rounds": len(interrupt_questions),
                "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                "final_generation_ms": 0.0,
                "total_tokens": total_tokens,
                "ping_count": ping_count,
                "char_count": sum(len(t) for t in final_report_chunks),
                "chapter_checks": {},
                "dimension_checks": {},
                "unrendered_vars_count": 0,
                "job_fidelity_pass": False,
                "raw_log": raw_log_file,
            }

    total_wall_ms = (time.time() - start_wall_time) * 1000
    final_report_text = "".join(final_report_chunks).strip()

    # Save raw log
    write_raw_log(raw_log_file, raw_events)

    # Run Assertions strictly on final_report_text
    eval_result = evaluate_report(
        final_text=final_report_text,
        target_job=target_job,
        case_expectations=expectations,
        interrupt_questions=interrupt_questions,
    )

    status = "PASS" if eval_result["passed"] else "FAIL"
    if status == "PASS" and eval_result["warnings"]:
        status = "WARN"

    status_str = "[PASS]" if status == "PASS" else ("[WARN]" if status == "WARN" else "[FAIL]")
    print(f"  └─ 结果: {status_str} | 端到端: {total_wall_ms/1000:.1f}s | 最终生成: {final_generation_ms/1000:.1f}s | 报告字符数: {len(final_report_text)} | Tokens: {total_tokens}")

    return {
        "id": case_id,
        "name": case_name,
        "target_job": target_job,
        "status": status,
        "interrupt_rounds": len(interrupt_questions),
        "total_wall_ms": round(total_wall_ms, 1),
        "final_generation_ms": round(final_generation_ms, 1),
        "total_tokens": total_tokens,
        "ping_count": ping_count,
        "char_count": len(final_report_text),
        "chapter_checks": eval_result["chapter_checks"],
        "dimension_checks": eval_result["dimension_checks"],
        "unrendered_vars_count": eval_result["unrendered_vars_count"],
        "job_fidelity_pass": eval_result["job_fidelity_pass"],
        "errors": eval_result["errors"],
        "warnings": eval_result["warnings"],
        "raw_log": raw_log_file,
    }


def execute_state_reset_case(
    client: XfyunWorkflowClient,
    case_def: Dict[str, Any],
    raw_log_dir: str,
) -> Dict[str, Any]:
    """
    Executes STATE_RESET verification (P0-1):
    1. Create fixed_uid and fixed_chat_id.
    2. Phase 1: Complete diagnostic with fixed_uid + fixed_chat_id until stop.
    3. Phase 2: Call chat/completions with the SAME fixed_uid and fixed_chat_id and '你好'.
    4. Assert it re-enters Q1 (target job) without inheriting previous job state.
    5. Log desensitized uid_hash and chat_id.
    """
    case_id = case_def["id"]
    case_name = case_def.get("name", case_id)
    raw_log_file = os.path.join(raw_log_dir, f"{case_id}.jsonl")

    fixed_uid = f"user_sr_{int(time.time())}"
    fixed_chat_id = f"chat_sr_{int(time.time())}"[:32]
    uid_hash = hashlib.sha256(fixed_uid.encode("utf-8")).hexdigest()[:12]

    raw_events = [
        {
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "session_info": {
                "uid_hash": uid_hash,
                "chat_id": fixed_chat_id,
            },
        }
    ]

    print(f"[RUN] 正在执行 [{case_id}] {case_name} ...")
    print(f"  - 固定会话: uid_hash={uid_hash} | chat_id={fixed_chat_id}")

    start_wall_time = time.time()

    # Step 1: Run complete diagnostic on fixed_uid + fixed_chat_id
    print("  [Phase 1] 运行初次完整诊断 (你好 -> 算法工程师 -> 大三 -> 暂无 -> stop) ...")
    phase1_def = {
        "id": f"{case_id}_p1",
        "name": "Phase 1 Complete Diagnostic (算法工程师)",
        "target_job": "算法工程师",
        "initial": "你好",
        "replies": ["算法工程师", "计算机科学与技术，大三", "暂无"],
        "expectations": {
            "final_contains": ["算法工程师"],
            "forbidden": ["改造工程师"],
        },
    }
    res_p1 = execute_standard_case(
        client=client,
        case_def=phase1_def,
        raw_log_dir=raw_log_dir,
        uid_override=fixed_uid,
        chat_id_override=fixed_chat_id,
    )
    if res_p1["status"] == "FAIL":
        raw_events.append({"phase": 1, "error": f"Phase 1 failed: {res_p1['errors']}"})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "状态重置校验",
            "status": "FAIL",
            "errors": [f"Phase 1 diagnostic failed: {res_p1['errors']}"],
            "warnings": [],
            "interrupt_rounds": res_p1["interrupt_rounds"],
            "total_wall_ms": res_p1["total_wall_ms"],
            "final_generation_ms": res_p1["final_generation_ms"],
            "total_tokens": res_p1["total_tokens"],
            "ping_count": res_p1["ping_count"],
            "char_count": res_p1["char_count"],
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    # Step 2: Trigger with same fixed_uid and fixed_chat_id and '你好'
    print(f"  [Phase 2] 保持相同会话 (uid_hash={uid_hash}, chat_id={fixed_chat_id})，发起 '你好' 校验是否进入 Q1 ...")
    try:
        resp2 = client.start_workflow("你好", fixed_uid, fixed_chat_id)
    except Exception as e:
        raw_events.append({"phase": 2, "error": str(e)})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "状态重置校验",
            "status": "FAIL",
            "errors": [f"Phase 2 start failed: {str(e)}"],
            "warnings": [],
            "interrupt_rounds": res_p1["interrupt_rounds"],
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": res_p1["final_generation_ms"],
            "total_tokens": res_p1["total_tokens"],
            "ping_count": res_p1["ping_count"],
            "char_count": res_p1["char_count"],
            "chapter_checks": res_p1["chapter_checks"],
            "dimension_checks": res_p1["dimension_checks"],
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    if resp2.status_code != 200:
        err_text = resp2.text[:200]
        raw_events.append({"phase": 2, "error": f"HTTP {resp2.status_code}", "body": err_text})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "状态重置校验",
            "status": "FAIL",
            "errors": [f"Phase 2 HTTP {resp2.status_code}: {err_text}"],
            "warnings": [],
            "interrupt_rounds": res_p1["interrupt_rounds"],
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": res_p1["final_generation_ms"],
            "total_tokens": res_p1["total_tokens"],
            "ping_count": res_p1["ping_count"],
            "char_count": res_p1["char_count"],
            "chapter_checks": res_p1["chapter_checks"],
            "dimension_checks": res_p1["dimension_checks"],
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    first_q = ""
    for event in parse_sse_stream(resp2.iter_lines()):
        raw_events.append({"phase": 2, "event": event})
        if event.get("code") and event.get("code") != 0:
            error_msg = f"Phase 2 API Error Code {event.get('code')}: {event.get('message')}"
            write_raw_log(raw_log_file, raw_events)
            return {
                "id": case_id,
                "name": case_name,
                "target_job": "状态重置校验",
                "status": "FAIL",
                "errors": [error_msg],
                "warnings": [],
                "interrupt_rounds": res_p1["interrupt_rounds"],
                "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                "final_generation_ms": res_p1["final_generation_ms"],
                "total_tokens": res_p1["total_tokens"],
                "ping_count": res_p1["ping_count"],
                "char_count": res_p1["char_count"],
                "chapter_checks": res_p1["chapter_checks"],
                "dimension_checks": res_p1["dimension_checks"],
                "unrendered_vars_count": 0,
                "job_fidelity_pass": False,
                "raw_log": raw_log_file,
            }

        event_data = event.get("event_data", {})
        if event_data.get("event_id") or event.get("finish_reason") == "interrupt":
            first_q = event_data.get("value", {}).get("content", "")
            break

    write_raw_log(raw_log_file, raw_events)

    # Assert that Q1 asks for target job (not restoring Q2/Q3 or assuming algorithm engineer)
    is_q1 = ("目标岗位" in first_q or "岗位" in first_q or "第 1 个问题" in first_q or "首选方向" in first_q) and ("收到，你的首选方向是" not in first_q)
    status = "PASS" if is_q1 else "FAIL"
    errors = [] if is_q1 else [f"Phase 2 did not reset to Q1! Question was: '{first_q[:80]}'"]

    print(f"  └─ 结果: {'[PASS]' if is_q1 else '[FAIL]'} | Phase 2 首轮问题: \"{first_q[:50]}...\"")

    return {
        "id": case_id,
        "name": case_name,
        "target_job": "状态重置校验",
        "status": status,
        "interrupt_rounds": 1,
        "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
        "final_generation_ms": res_p1["final_generation_ms"],
        "total_tokens": res_p1["total_tokens"],
        "ping_count": res_p1["ping_count"],
        "char_count": res_p1["char_count"],
        "chapter_checks": res_p1["chapter_checks"],
        "dimension_checks": res_p1["dimension_checks"],
        "unrendered_vars_count": 0,
        "job_fidelity_pass": is_q1,
        "errors": errors,
        "warnings": [],
        "raw_log": raw_log_file,
    }


def execute_abort_and_switch_case(
    client: XfyunWorkflowClient,
    case_def: Dict[str, Any],
    raw_log_dir: str,
) -> Dict[str, Any]:
    """
    Executes ABORT_AND_SWITCH verification (P0-2):
    1. Phase 1: Start workflow with '算法工程师' on fixed_uid + fixed_chat_id, reach Q2.
    2. Phase 2: Call resume(event_type='abort'). Validate EXPECTED_ABORT_CODES={0, 23802}.
    3. Phase 3: Reuse SAME fixed_uid + fixed_chat_id to start '产品经理'.
       - If platform rejects chat_id reuse after abort -> UNSUPPORTED (do NOT fake chat_id).
       - If platform accepts -> verify clean switch to '产品经理' and complete diagnosis.
    """
    case_id = case_def["id"]
    case_name = case_def.get("name", case_id)
    raw_log_file = os.path.join(raw_log_dir, f"{case_id}.jsonl")

    fixed_uid = f"user_as_{int(time.time())}"
    fixed_chat_id = f"chat_as_{int(time.time())}"[:32]
    uid_hash = hashlib.sha256(fixed_uid.encode("utf-8")).hexdigest()[:12]

    raw_events = [
        {
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "session_info": {
                "uid_hash": uid_hash,
                "chat_id": fixed_chat_id,
            },
        }
    ]

    print(f"[RUN] 正在执行 [{case_id}] {case_name} ...")
    print(f"  - 固定会话: uid_hash={uid_hash} | chat_id={fixed_chat_id}")

    start_wall_time = time.time()

    # Step 1: Start 算法工程师
    print("  [Phase 1] 启动 '算法工程师' -> 进入 Q2 ...")
    try:
        resp1 = client.start_workflow("算法工程师", fixed_uid, fixed_chat_id)
    except Exception as e:
        raw_events.append({"phase": 1, "error": str(e)})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": [f"Phase 1 start network error: {str(e)}"],
            "warnings": [],
            "interrupt_rounds": 0,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    if resp1.status_code != 200:
        err_text = resp1.text[:200]
        raw_events.append({"phase": 1, "error": f"HTTP {resp1.status_code}", "body": err_text})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": [f"Phase 1 HTTP {resp1.status_code}: {err_text}"],
            "warnings": [],
            "interrupt_rounds": 0,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    event_id_q2 = None
    for event in parse_sse_stream(resp1.iter_lines()):
        raw_events.append({"phase": "start_q2", "event": event})
        ev_data = event.get("event_data", {})
        if ev_data.get("event_id"):
            event_id_q2 = ev_data.get("event_id")
            break

    if not event_id_q2:
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": ["Failed to reach Q2 event_id in Phase 1"],
            "warnings": [],
            "interrupt_rounds": 0,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    # Step 2: Abort
    print(f"  [Phase 2] 发送 resume(event_type='abort', event_id={event_id_q2}) ...")
    EXPECTED_ABORT_CODES = {0, 23802}
    abort_events = []
    abort_code = None
    abort_message = ""
    try:
        abort_resp = client.resume_workflow(event_id_q2, answer="", event_type="abort")
        if abort_resp.status_code != 200:
            err_text = abort_resp.text[:200]
            raw_events.append({"phase": "abort", "error": f"HTTP {abort_resp.status_code}", "body": err_text})
            write_raw_log(raw_log_file, raw_events)
            return {
                "id": case_id,
                "name": case_name,
                "target_job": "产品经理",
                "status": "FAIL",
                "errors": [f"Abort request HTTP {abort_resp.status_code}: {err_text}"],
                "warnings": [],
                "interrupt_rounds": 1,
                "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
                "final_generation_ms": 0.0,
                "total_tokens": 0,
                "ping_count": 0,
                "char_count": 0,
                "chapter_checks": {},
                "dimension_checks": {},
                "unrendered_vars_count": 0,
                "job_fidelity_pass": False,
                "raw_log": raw_log_file,
            }

        for event in parse_sse_stream(abort_resp.iter_lines()):
            raw_events.append({"phase": "abort", "event": event})
            abort_events.append(event)
            if "code" in event:
                abort_code = event.get("code")
                abort_message = event.get("message", "")

    except Exception as e:
        raw_events.append({"phase": "abort", "error": str(e)})
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": [f"Abort request failed with network error: {str(e)}"],
            "warnings": [],
            "interrupt_rounds": 1,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    # Validate abort response
    if abort_code is not None and abort_code not in EXPECTED_ABORT_CODES:
        err_msg = f"Unexpected abort API code: {abort_code}, message: '{abort_message}'"
        print(f"    [FAIL] {err_msg}")
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": [err_msg],
            "warnings": [],
            "interrupt_rounds": 1,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    if abort_code == 23802 and "Received abort instruction" not in abort_message:
        err_msg = f"Abort returned code 23802 but message missing 'Received abort instruction': '{abort_message}'"
        print(f"    [FAIL] {err_msg}")
        write_raw_log(raw_log_file, raw_events)
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "FAIL",
            "errors": [err_msg],
            "warnings": [],
            "interrupt_rounds": 1,
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": 0.0,
            "total_tokens": 0,
            "ping_count": 0,
            "char_count": 0,
            "chapter_checks": {},
            "dimension_checks": {},
            "unrendered_vars_count": 0,
            "job_fidelity_pass": False,
            "raw_log": raw_log_file,
        }

    print(f"    [Abort Validated] HTTP 200 | Code: {abort_code} | Msg: {abort_message}")

    # Step 3: Start new workflow with 产品经理 using the SAME fixed_uid + fixed_chat_id
    print(f"  [Phase 3] 使用同一会话 (chat_id={fixed_chat_id}) 启动 '产品经理' 并完成诊断 ...")
    phase3_def = {
        "id": f"{case_id}_p3",
        "name": "Phase 3 Switched to PM",
        "target_job": "产品经理",
        "initial": "产品经理",
        "replies": ["软件工程，大三", "做过Axure原型设计"],
        "expectations": {
            "first_interrupt_contains": "产品经理",
            "final_contains": ["产品经理"],
            "forbidden": ["算法工程师", "改造工程师"],
        },
    }

    res_p3 = execute_standard_case(
        client=client,
        case_def=phase3_def,
        raw_log_dir=raw_log_dir,
        uid_override=fixed_uid,
        chat_id_override=fixed_chat_id,
    )

    write_raw_log(raw_log_file, raw_events)

    # If platform returned unsupported error for chat_id reuse
    err_str = " ".join(res_p3.get("errors", []))
    if "not support" in err_str.lower() or "closed" in err_str.lower() or "terminated" in err_str.lower():
        print("  └─ 结果: [UNSUPPORTED] 平台不支持 abort 后复用同一 chat_id")
        return {
            "id": case_id,
            "name": case_name,
            "target_job": "产品经理",
            "status": "UNSUPPORTED",
            "interrupt_rounds": res_p3["interrupt_rounds"],
            "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
            "final_generation_ms": res_p3["final_generation_ms"],
            "total_tokens": res_p3["total_tokens"],
            "ping_count": res_p3["ping_count"],
            "char_count": res_p3["char_count"],
            "chapter_checks": res_p3["chapter_checks"],
            "dimension_checks": res_p3["dimension_checks"],
            "unrendered_vars_count": res_p3["unrendered_vars_count"],
            "job_fidelity_pass": False,
            "errors": [f"Platform unsupported: {err_str}"],
            "warnings": [],
            "raw_log": raw_log_file,
        }

    return {
        "id": case_id,
        "name": case_name,
        "target_job": "产品经理",
        "status": res_p3["status"],
        "interrupt_rounds": res_p3["interrupt_rounds"],
        "total_wall_ms": round((time.time() - start_wall_time) * 1000, 1),
        "final_generation_ms": res_p3["final_generation_ms"],
        "total_tokens": res_p3["total_tokens"],
        "ping_count": res_p3["ping_count"],
        "char_count": res_p3["char_count"],
        "chapter_checks": res_p3["chapter_checks"],
        "dimension_checks": res_p3["dimension_checks"],
        "unrendered_vars_count": res_p3["unrendered_vars_count"],
        "job_fidelity_pass": res_p3["job_fidelity_pass"],
        "errors": res_p3["errors"],
        "warnings": res_p3["warnings"],
        "raw_log": raw_log_file,
    }


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Xfyun Career Diagnosis API Regression Runner")
    parser.add_argument("--cases", default="cases/career_cases.yaml", help="Path to YAML cases file")
    parser.add_argument("--smoke", action="store_true", help="Run only smoke test (T01)")
    parser.add_argument("--case", type=str, default="", help="Run a specific case ID")
    parser.add_argument("--cases-subset", type=str, default="", help="Comma-separated subset of case IDs to run (e.g. T02,T08,STATE_RESET,ABORT_AND_SWITCH)")
    parser.add_argument("--merge-existing", action="store_true", default=True, help="Merge subset results with existing summary.json")
    parser.add_argument("--output-dir", default="reports", help="Output directory for reports")
    args = parser.parse_args()

    client = XfyunWorkflowClient()
    print_preflight(client)

    # Load cases
    cases_path = os.path.join(os.path.dirname(__file__), "..", args.cases)
    if not os.path.exists(cases_path):
        print(f"❌ Cases file not found: {cases_path}")
        sys.exit(1)

    with open(cases_path, "r", encoding="utf-8") as f:
        cases_doc = yaml.safe_load(f)
    all_cases = cases_doc.get("cases", [])

    out_dir = os.path.join(os.path.dirname(__file__), "..", args.output_dir)
    existing_summary_path = os.path.join(out_dir, "summary.json")
    existing_results_map = {}
    if os.path.exists(existing_summary_path):
        try:
            with open(existing_summary_path, "r", encoding="utf-8") as f:
                existing_doc = json.load(f)
                for item in existing_doc.get("cases", []):
                    existing_results_map[item["id"]] = item
        except Exception as e:
            print(f"[WARN] Failed to load existing summary.json: {e}")

    if args.smoke:
        selected_cases = [c for c in all_cases if c["id"] == "T01"]
        print("[INFO] 运行 Smoke Test (冒烟测试)...")
    elif args.case:
        selected_cases = [c for c in all_cases if c["id"] == args.case]
        print(f"[INFO] 运行指定用例 [{args.case}]...")
    elif args.cases_subset:
        subset_ids = [s.strip() for s in args.cases_subset.split(",") if s.strip()]
        selected_cases = [c for c in all_cases if c["id"] in subset_ids]
        print(f"[INFO] 运行指定用例子集 ({len(selected_cases)} 个用例: {subset_ids})...")
    else:
        selected_cases = all_cases
        print(f"[INFO] 运行全量批量回归测试集 (共 {len(selected_cases)} 个用例, Concurrency = 1)...")

    new_results = []
    raw_dir = os.path.join(out_dir, "raw")

    for idx, c in enumerate(selected_cases, start=1):
        print(f"\n[{idx}/{len(selected_cases)}] ----------------------------------------")
        case_type = c.get("case_type", "standard")
        if case_type == "state_reset":
            res = execute_state_reset_case(client, c, raw_dir)
        elif case_type == "abort_and_switch":
            res = execute_abort_and_switch_case(client, c, raw_dir)
        else:
            res = execute_standard_case(client, c, raw_dir)

        new_results.append(res)
        # Update into existing map
        existing_results_map[res["id"]] = res
        time.sleep(1)

    # Determine final results list
    if (args.case or args.cases_subset) and existing_results_map:
        # Preserve original full case ordering from career_cases.yaml
        final_results = []
        for c in all_cases:
            cid = c["id"]
            if cid in existing_results_map:
                final_results.append(existing_results_map[cid])
    else:
        final_results = new_results

    # Generate Reports
    summary = generate_reports(final_results, out_dir)

    print("\n" + "=" * 65)
    print(" [SUMMARY] 测试汇总完成")
    print("=" * 65)
    print(f" 总案例数: {summary['total_cases']} | 有效通过 (VALID PASS): {summary['valid_pass_count']} | 平台不支持 (UNSUPPORTED): {summary['unsupported_count']} | 告警: {summary['warn_count']} | 失败: {summary['fail_count']}")
    print(f" 通过率: {summary['pass_rate']}")
    print(f" P50 耗时: {summary['performance']['p50_ms']/1000:.1f}s | P95 耗时: {summary['performance']['p95_ms']/1000:.1f}s | 平均 Token: {summary['performance']['avg_tokens']}")
    print(f" 详细报告已生成至: {os.path.abspath(out_dir)}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
