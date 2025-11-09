"""Minimal wrapper around OpenAI's chat completions endpoint."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    role: str
    content: str

    def as_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


class ChatClientError(Exception):
    """Custom error raised for chat API problems."""


class ChatClient:
    """
    Simple OpenAI ChatGPT client using the REST API.

    Parameters
    ----------
    api_key:
        OpenAI API key (beginning with ``sk-``). Required for requests.
    default_model:
        Chat model name to use when one is not supplied explicitly.
    timeout:
        Request timeout (seconds).
    """

    def __init__(self, api_key: Optional[str], default_model: str = "gpt-4o-mini", timeout: int = 60) -> None:
        self.api_key = api_key
        self.default_model = default_model
        self.timeout = timeout
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self._session = requests.Session()

    def update_api_key(self, api_key: Optional[str]) -> None:
        """Update the client's API key."""
        self.api_key = api_key

    def send_chat(
        self,
        messages: List[ChatMessage],
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a chat completion request and return the assistant's reply.

        Raises
        ------
        ChatClientError
            If the API key is missing or the request fails.
        """
        if not self.api_key:
            raise ChatClientError("OpenAI API key is not configured. Please set it before sending messages.")

        payload = {
            "model": model or self.default_model,
            "messages": [message.as_dict() for message in messages],
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = self._session.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.HTTPError as exc:
            detail = self._extract_error_detail(exc.response)
            raise ChatClientError(detail) from exc
        except requests.RequestException as exc:
            raise ChatClientError(f"Network error while calling OpenAI: {exc}") from exc

        try:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            raise ChatClientError("Unexpected response from OpenAI.") from exc

    @staticmethod
    def _extract_error_detail(response: Optional[requests.Response]) -> str:
        if response is None:
            return "HTTP error without a response body."

        try:
            data = response.json()
            message = data.get("error", {}).get("message")
            if message:
                return f"OpenAI API error: {message}"
        except json.JSONDecodeError:
            logger.debug("Failed to parse OpenAI error response: %s", response.text)

        return f"OpenAI API returned {response.status_code}: {response.text[:200]}"

