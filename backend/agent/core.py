"""
Core agent loop, powered by Groq.

The pattern:
  1. Send conversation + tool schemas to the model.
  2. If the model wants to call tool(s), run them and feed results back as
     role="tool" messages.
  3. Repeat until the model gives a final text answer (no more tool calls).

Edit SYSTEM_PROMPT below once you know your actual problem statement -
everything else here should just work.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from agent.tools import get_schemas, call_tool

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Groq's fast, tool-capable model. Swap to "llama-3.1-8b-instant" for even
# faster/cheaper responses if 70b is overkill for your task, or check
# https://console.groq.com/docs/models for the current model list.
MODEL = "openai/gpt-oss-120b"
MAX_TOKENS = 2048
MAX_TURNS = 10  # safety limit so a stuck loop doesn't burn all your API credits

# --- EDIT THIS when you get the real problem statement ---------------------
SYSTEM_PROMPT = """You are a helpful AI agent competing in a hackathon.
You have access to tools: use them whenever they'd help answer accurately
rather than guessing. Think step by step. When you have enough information,
give a clear, direct final answer.
"""
# -----------------------------------------------------------------------


def call_model(messages: list):
    """The only function you need to change to swap providers."""
    return client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        tools=get_schemas(),
        tool_choice="auto",
        messages=messages,
    )


def run_agent(user_message: str, verbose: bool = True) -> str:
    """Run the agent loop for a single user message. Returns the final text answer."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for turn in range(MAX_TURNS):
        response = call_model(messages)
        choice = response.choices[0]
        msg = choice.message

        if not msg.tool_calls:
            # Model is done - return its final text
            if verbose:
                print(f"[turn {turn}] final answer: {msg.content}")
            return msg.content or "(no text response)"

        if verbose and msg.content:
            print(f"[turn {turn}] model says: {msg.content}")

        # Model wants to call one or more tools.
        # Append the assistant turn exactly as returned (needed for tool_call_id matching).
        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )

        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments)
            except json.JSONDecodeError:
                args = {}

            if verbose:
                print(f"[turn {turn}] calling tool: {tc.function.name}({args})")

            result = call_tool(tc.function.name, args)

            if verbose:
                print(f"[turn {turn}] tool result: {result[:300]}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                }
            )

    return "Reached max turns without a final answer - check for a loop."


if __name__ == "__main__":
    print("Agent starter CLI (Groq). Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        answer = run_agent(user_input)
        print(f"\nAgent: {answer}\n")
