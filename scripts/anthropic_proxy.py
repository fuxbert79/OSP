#!/usr/bin/env python3
"""
Anthropic zu OpenAI Proxy
=========================

Macht die Anthropic API OpenAI-kompatibel für Open WebUI.

Port: 4000
Endpunkte:
- /v1/models - Liste verfügbare Modelle
- /v1/chat/completions - Chat Completions (OpenAI-Format)

Starten:
  python3 anthropic_proxy.py

Autor: AL
Stand: 2025-12-14
"""

import os
import json
import logging
from flask import Flask, request, jsonify, Response
import anthropic

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)

# Anthropic Client
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable required")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Verfügbare Modelle
MODELS = {
    "osp-claude": "claude-sonnet-4-20250514",
    "claude-sonnet": "claude-sonnet-4-20250514",
    "claude-haiku": "claude-3-5-haiku-20241022",
}


@app.route("/v1/models", methods=["GET"])
def list_models():
    """Liste verfügbare Modelle im OpenAI-Format."""
    models = [
        {
            "id": model_id,
            "object": "model",
            "created": 1700000000,
            "owned_by": "anthropic",
        }
        for model_id in MODELS.keys()
    ]
    return jsonify({"object": "list", "data": models})


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """Chat Completions im OpenAI-Format."""
    data = request.json

    # Model-Mapping
    model_id = data.get("model", "osp-claude")
    anthropic_model = MODELS.get(model_id, "claude-sonnet-4-20250514")

    # Messages konvertieren
    messages = data.get("messages", [])
    system_prompt = None
    anthropic_messages = []

    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Streaming?
    stream = data.get("stream", False)
    max_tokens = data.get("max_tokens", 4096)

    logger.info(f"Request: model={model_id} -> {anthropic_model}, stream={stream}")

    try:
        if stream:
            # Streaming Response
            def generate():
                with client.messages.stream(
                    model=anthropic_model,
                    max_tokens=max_tokens,
                    system=system_prompt or "",
                    messages=anthropic_messages
                ) as stream_response:
                    for text in stream_response.text_stream:
                        chunk = {
                            "id": "chatcmpl-proxy",
                            "object": "chat.completion.chunk",
                            "created": 1700000000,
                            "model": model_id,
                            "choices": [{
                                "index": 0,
                                "delta": {"content": text},
                                "finish_reason": None
                            }]
                        }
                        yield f"data: {json.dumps(chunk)}\n\n"

                    # Final chunk
                    final_chunk = {
                        "id": "chatcmpl-proxy",
                        "object": "chat.completion.chunk",
                        "created": 1700000000,
                        "model": model_id,
                        "choices": [{
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop"
                        }]
                    }
                    yield f"data: {json.dumps(final_chunk)}\n\n"
                    yield "data: [DONE]\n\n"

            return Response(generate(), mimetype="text/event-stream")

        else:
            # Non-Streaming Response
            response = client.messages.create(
                model=anthropic_model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=anthropic_messages
            )

            return jsonify({
                "id": "chatcmpl-proxy",
                "object": "chat.completion",
                "created": 1700000000,
                "model": model_id,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.content[0].text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            })

    except Exception as e:
        logger.error(f"API Error: {e}")
        return jsonify({"error": {"message": str(e), "type": "api_error"}}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health Check."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    logger.info("Starting Anthropic Proxy on port 4000...")
    logger.info(f"Available models: {list(MODELS.keys())}")
    app.run(host="0.0.0.0", port=4000, debug=False)
