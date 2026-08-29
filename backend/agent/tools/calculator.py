"""
Simple calculator tool. Use this as a TEMPLATE for writing new tools:
1. Write a function that does the work and returns a string.
2. Write a JSON schema describing its inputs.
3. Register both in agent/tools/__init__.py
"""

import math

SCHEMA = {
    "name": "calculator",
    "description": (
        "Evaluate a math expression. Supports +, -, *, /, **, parentheses, "
        "and functions like sqrt, sin, cos, log. Use this for any arithmetic "
        "instead of doing math yourself."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A math expression, e.g. '(4 + 5) * 3' or 'sqrt(16)'",
            }
        },
        "required": ["expression"],
    },
}

_ALLOWED_NAMES = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}


def run(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, _ALLOWED_NAMES)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
