"""
iFlytek Xingchen Workflow API Client.
"""

import os
import time
import requests
from typing import Generator, Dict, Any, Optional
from src.sse_parser import parse_sse_stream


class XfyunWorkflowClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        flow_id: Optional[str] = None,
        chat_url: Optional[str] = None,
        resume_url: Optional[str] = None,
        connect_timeout: int = 15,
        read_timeout: int = 300,
    ):
        self.api_key = api_key or os.getenv("XFYUN_API_KEY", "")
        self.api_secret = api_secret or os.getenv("XFYUN_API_SECRET", "")
        self.flow_id = flow_id or os.getenv("XFYUN_FLOW_ID", "")
        self.chat_url = chat_url or os.getenv(
            "XFYUN_CHAT_URL",
            "https://xingchen-api.xf-yun.com/workflow/v1/chat/completions",
        )
        self.resume_url = resume_url or os.getenv(
            "XFYUN_RESUME_URL", "https://xingchen-api.xf-yun.com/workflow/v1/resume"
        )
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

        if not self.api_key or not self.api_secret or not self.flow_id:
            raise ValueError(
                "Missing required XFYUN API credentials (API_KEY, API_SECRET, FLOW_ID)."
            )

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def start_workflow(
        self, initial_text: str, uid: str, chat_id: str
    ) -> requests.Response:
        """
        Starts the workflow execution session.
        """
        payload = {
            "flow_id": self.flow_id,
            "uid": uid,
            "parameters": {"AGENT_USER_INPUT": initial_text},
            "stream": True,
            "chat_id": chat_id,
        }
        response = requests.post(
            self.chat_url,
            json=payload,
            headers=self.headers,
            stream=True,
            timeout=(self.connect_timeout, self.read_timeout),
        )
        return response

    def resume_workflow(
        self, event_id: str, answer: str = "", event_type: str = "resume"
    ) -> requests.Response:
        """
        Resumes or aborts the interrupted workflow with user response.
        """
        payload = {
            "event_id": event_id,
            "event_type": event_type,
            "content": answer,
        }
        response = requests.post(
            self.resume_url,
            json=payload,
            headers=self.headers,
            stream=True,
            timeout=(self.connect_timeout, self.read_timeout),
        )
        return response
