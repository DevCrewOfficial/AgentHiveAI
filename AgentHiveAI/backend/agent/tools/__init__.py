from . import shipment


# These are the tools given to Groq
TOOLS = shipment.TOOLS


def execute_tool(name: str, tool_input: dict):
    """Execute a shipment tool by name."""

    if name not in shipment.FUNCTIONS:
        return {
            "success": False,
            "error": f"Unknown tool: {name}"
        }

    try:
        result = shipment.FUNCTIONS[name](**tool_input)
        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }