"""
title: Anthropic Claude 4.5
author: OSP Team (AL)
author_url: https://schneider-kabelsatzbau.de
version: 0.3.3
description: Anthropic Claude 4.5 Models (Opus, Sonnet, Haiku) - Fixed temperature/top_p conflict
license: MIT
"""

import os
import json
import httpx
from typing import Generator, Iterator, List, Union

from pydantic import BaseModel, Field


class Pipe:
    """Anthropic Claude 4.5 Manifold Pipe for Open WebUI"""

    class Valves(BaseModel):
        ANTHROPIC_API_KEY: str = Field(
            default="",
            description="Anthropic API Key (sk-ant-...)"
        )
        USE_TEMPERATURE: bool = Field(
            default=True,
            description="True = use temperature, False = use top_p (Claude 4.5 only allows one)"
        )

    def __init__(self):
        self.type = "manifold"
        self.id = "anthropic"
        self.name = "Anthropic: "
        self.valves = self.Valves(
            ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY", "")
        )

    def get_anthropic_models(self) -> List[dict]:
        """Return Claude 4.5 models only"""
        return [
            {"id": "claude-sonnet-4-5-20250929", "name": "claude-4.5-sonnet"},
            {"id": "claude-haiku-4-5-20251001", "name": "claude-4.5-haiku"},
            {"id": "claude-opus-4-5-20251101", "name": "claude-4.5-opus"},
        ]

    def pipes(self) -> List[dict]:
        """Return available models"""
        return self.get_anthropic_models()

    def process_image(self, image_data: dict) -> dict:
        """Process image data for Anthropic API format"""
        if image_data.get("url", "").startswith("data:"):
            # Base64 encoded image
            mime_type, base64_data = image_data["url"].split(",", 1)
            media_type = mime_type.split(":")[1].split(";")[0]
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_data,
                },
            }
        else:
            # URL-based image
            return {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": image_data.get("url", ""),
                },
            }

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        """Main pipe method - processes requests to Anthropic API"""

        # Extract and fix model_id FIRST (before any usage)
        raw_model = body.get("model", "")
        if "." in raw_model:
            model_id = raw_model[raw_model.find(".") + 1:]
        else:
            model_id = raw_model

        # Fallback to default model if empty
        if not model_id:
            model_id = "claude-sonnet-4-5-20250929"

        # Process messages
        messages = body.get("messages", [])
        processed_messages = []
        system_message = None

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            # Handle system messages separately
            if role == "system":
                system_message = content
                continue

            # Process content (text or multimodal)
            if isinstance(content, list):
                # Multimodal content
                processed_content = []
                for item in content:
                    if item.get("type") == "text":
                        processed_content.append({
                            "type": "text",
                            "text": item.get("text", "")
                        })
                    elif item.get("type") == "image_url":
                        processed_content.append(
                            self.process_image(item.get("image_url", {}))
                        )
                processed_messages.append({
                    "role": role,
                    "content": processed_content
                })
            else:
                # Simple text content
                processed_messages.append({
                    "role": role,
                    "content": str(content)
                })

        # Build payload - CRITICAL: Don't set both temperature AND top_p!
        payload = {
            "model": model_id,
            "messages": processed_messages,
            "max_tokens": body.get("max_tokens", 8192),
            "stream": body.get("stream", False),
        }

        # Add system message if present
        if system_message:
            payload["system"] = str(system_message)

        # Add stop sequences if present
        stop_sequences = body.get("stop", [])
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences

        # CRITICAL FIX: Only use temperature OR top_p, never both!
        # Claude 4.5 models throw error if both are specified
        if self.valves.USE_TEMPERATURE:
            temp = body.get("temperature")
            if temp is not None:
                payload["temperature"] = float(temp)
            else:
                payload["temperature"] = 0.7
        else:
            top_p = body.get("top_p")
            if top_p is not None:
                payload["top_p"] = float(top_p)
            else:
                payload["top_p"] = 0.9

        # Prepare headers
        headers = {
            "x-api-key": self.valves.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        url = "https://api.anthropic.com/v1/messages"

        try:
            if payload.get("stream", False):
                # Streaming response
                return self._stream_response(url, headers, payload)
            else:
                # Non-streaming response
                return self._sync_response(url, headers, payload)
        except Exception as e:
            return f"Error: {str(e)}"

    def _sync_response(self, url: str, headers: dict, payload: dict) -> str:
        """Handle non-streaming response"""
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                error_detail = response.text
                return f"API Error ({response.status_code}): {error_detail}"

            data = response.json()

            # Extract text from response
            content = data.get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "")
            return ""

    def _stream_response(self, url: str, headers: dict, payload: dict) -> Generator:
        """Handle streaming response"""
        with httpx.Client(timeout=120.0) as client:
            with client.stream("POST", url, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    yield f"API Error ({response.status_code})"
                    return

                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            event_type = data.get("type", "")

                            if event_type == "content_block_delta":
                                delta = data.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    yield delta.get("text", "")
                            elif event_type == "message_stop":
                                break
                        except json.JSONDecodeError:
                            continue
