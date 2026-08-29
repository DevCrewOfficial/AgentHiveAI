"""
File read/write tool, sandboxed to the ./data directory so the agent
can't wander around the filesystem.
"""

import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

SCHEMA = {
    "name": "file_io",
    "description": (
        "Read or write a text file inside the sandboxed data/ directory. "
        "Use this to save intermediate results or read provided data files."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["read", "write", "list"]},
            "filename": {
                "type": "string",
                "description": "Filename relative to data/, e.g. 'notes.txt'",
            },
            "content": {
                "type": "string",
                "description": "Content to write (required for action='write')",
            },
        },
        "required": ["action"],
    },
}


def _safe_path(filename: str) -> str:
    path = os.path.normpath(os.path.join(DATA_DIR, filename))
    if not path.startswith(DATA_DIR):
        raise ValueError("Path escapes sandboxed data directory")
    return path


def run(action: str, filename: str = None, content: str = None) -> str:
    try:
        if action == "list":
            files = os.listdir(DATA_DIR)
            return "\n".join(files) if files else "data/ is empty"

        if not filename:
            return "Error: filename is required for read/write"

        path = _safe_path(filename)

        if action == "read":
            if not os.path.exists(path):
                return f"Error: {filename} does not exist"
            with open(path, "r") as f:
                return f.read()

        if action == "write":
            if content is None:
                return "Error: content is required for action='write'"
            with open(path, "w") as f:
                f.write(content)
            return f"Wrote {len(content)} chars to {filename}"

        return f"Unknown action: {action}"
    except Exception as e:
        return f"File operation failed: {e}"
