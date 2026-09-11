"""
SSE (Server-Sent Events) stream parser for iFlytek Xingchen Workflow API.
"""

import json
from typing import Generator, Dict, Any, Optional


def parse_sse_stream(response_iter_lines) -> Generator[Dict[str, Any], None, None]:
    """
    Parses SSE response stream line by line and yields event payloads.
    
    Expected format:
      data: {"id":"...","choices":[{"delta":{"content":"..."},"finish_reason":"interrupt"}],"event_data":{"event_id":"..."},...}
    """
    for line in response_iter_lines:
        if not line:
            continue
        if isinstance(line, bytes):
            line_str = line.decode("utf-8", errors="replace").strip()
        else:
            line_str = line.strip()
            
        if not line_str:
            continue
            
        if line_str.startswith("data:"):
            data_str = line_str[5:].strip()
            if data_str == "[DONE]":
                yield {"finish_reason": "stop", "content": "", "is_done": True}
                continue
            try:
                parsed = json.loads(data_str)
                yield parsed
            except json.JSONDecodeError:
                yield {"raw_data": data_str, "error": "json_decode_error"}
        elif line_str.startswith("event:"):
            event_name = line_str[6:].strip()
            # event type annotation
            pass
        elif line_str.startswith("id:"):
            # sse id
            pass
        elif line_str.startswith("ping"):
            yield {"finish_reason": "ping"}
