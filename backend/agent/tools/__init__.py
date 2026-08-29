"""
Tool registry. To add a new tool tomorrow:

1. Create agent/tools/your_tool.py with a SCHEMA dict and a run(**kwargs) function
   (see calculator.py for the simplest example).
2. Import it below and add it to TOOLS.

That's it - the agent loop in core.py will pick it up automatically.
"""

from . import calculator
from . import web_search
from . import http_request
from . import file_io
from . import rag

# Registry: name -> module (must have .SCHEMA and .run)
TOOLS = {
    calculator.SCHEMA["name"]: calculator,
    web_search.SCHEMA["name"]: web_search,
    http_request.SCHEMA["name"]: http_request,
    file_io.SCHEMA["name"]: file_io,
    rag.SCHEMA["name"]: rag,
}


def get_schemas():
    """
    Return tool schemas in Groq/OpenAI function-calling format:
      {"type": "function", "function": {"name", "description", "parameters"}}

    Each tool module still just defines a simple SCHEMA dict with
    name/description/input_schema - this wraps it into the shape Groq expects.
    """
    schemas = []
    for mod in TOOLS.values():
        s = mod.SCHEMA
        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": s["name"],
                    "description": s["description"],
                    "parameters": s["input_schema"],
                },
            }
        )
    return schemas


def call_tool(name: str, tool_input: dict) -> str:
    """Execute a tool by name and return its string output."""
    if name not in TOOLS:
        return f"Error: unknown tool '{name}'"
    try:
        return TOOLS[name].run(**tool_input)
    except Exception as e:
        return f"Error running tool '{name}': {e}"
