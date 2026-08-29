import json
import time
from groq import Groq

from .tools import TOOLS, execute_tool
from .prompt import SYSTEM_PROMPT


MODEL = "qwen/qwen3.6-27b"


def run_agent(client, user_input, history, trail):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + history

    if user_input:
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    latency_ms = int((time.time() - start) * 1000)

    tokens = (
        response.usage.total_tokens
        if response.usage
        else None
    )

    msg = response.choices[0].message

    # -----------------------------------------
    # Agent wants to use one or more tools
    # -----------------------------------------

    if msg.tool_calls:

        history.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in msg.tool_calls
                ]
            }
        )

        for call in msg.tool_calls:

            args = json.loads(call.function.arguments)

            result = execute_tool(
                call.function.name,
                args
            )

            # Save execution information
            trail.append(
                {
                    "reasoning": msg.content or "",
                    "tool": call.function.name,
                    "args": args,
                    "result": result,
                    "tokens": tokens,
                    "latency_ms": latency_ms
                }
            )

            # Give tool result back to the model
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                }
            )

        # Ask the model what to do next
        return run_agent(
            client,
            None,
            history,
            trail
        )

    # -----------------------------------------
    # Agent has final answer
    # -----------------------------------------

    history.append(
        {
            "role": "assistant",
            "content": msg.content or ""
        }
    )

    return msg.content or "", history, trail