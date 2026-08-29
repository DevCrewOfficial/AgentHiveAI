"""
Generic HTTP request tool. Handy when your problem statement involves hitting
some external API (weather, finance, custom hackathon-provided API, etc).
"""

import json
import requests

SCHEMA = {
    "name": "http_request",
    "description": (
        "Make an HTTP request to a given URL. Use this to call external APIs. "
        "Returns the response body as text (truncated if very long)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Full URL to request"},
            "method": {
                "type": "string",
                "enum": ["GET", "POST", "PUT", "DELETE"],
                "description": "HTTP method, default GET",
            },
            "headers": {
                "type": "object",
                "description": "Optional headers as a JSON object",
            },
            "body": {
                "type": "object",
                "description": "Optional JSON body for POST/PUT requests",
            },
        },
        "required": ["url"],
    },
}


def run(url: str, method: str = "GET", headers: dict = None, body: dict = None) -> str:
    try:
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers=headers or {},
            json=body if body else None,
            timeout=15,
        )
        text = resp.text
        if len(text) > 3000:
            text = text[:3000] + "... [truncated]"
        return f"Status: {resp.status_code}\nBody: {text}"
    except Exception as e:
        return f"Request failed: {e}"
