# Hackathon Agent Starter

A minimal, hackable agent skeleton so you can plug in your actual problem statement fast.

## What's inside

```
agent-starter/
├── agent/
│   ├── core.py          # The agent loop (plan -> tool call -> observe -> respond)
│   ├── tools/
│   │   ├── __init__.py  # Tool registry - add new tools here
│   │   ├── calculator.py
│   │   ├── web_search.py
│   │   ├── http_request.py
│   │   ├── file_io.py
│   │   └── rag.py       # Simple local document search (no vector DB needed)
├── app.py                # Streamlit demo UI
├── requirements.txt
├── .env.example
└── README.md
```

## Setup (do this tonight)

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then fill in your API key(s)
```

Get a free Groq API key at https://console.groq.com/keys

## Run it

```bash
# CLI test
python -m agent.core

# Streamlit demo
streamlit run app.py
```

## Tomorrow, when you get the problem statement

1. Look in `agent/tools/` — see if an existing tool covers part of what you need. Edit it.
2. Add a new tool: copy `agent/tools/calculator.py` as a template. Every tool is just:
   - a Python function
   - a JSON schema describing its inputs
   - registered in `agent/tools/__init__.py`
3. Update the system prompt in `agent/core.py` to describe the specific task.
4. Wire up `app.py` if you want a nicer demo than the CLI.

That's it — the loop, error handling, and logging are already done.

## Swapping providers / models

Everything routes through `agent/core.py::call_model()`. It's using Groq's
`llama-3.3-70b-versatile` by default (fast + supports tool calling). To change models,
just edit `MODEL` at the top of `agent/core.py` — see https://console.groq.com/docs/models
for the current list of tool-capable models. Since Groq's API is OpenAI-compatible,
switching to OpenAI later is a small change (same message/tool-call shape, different client).

## Tips for the actual hackathon

- Don't over-engineer. Judges care about the demo working, not architecture purity.
- Keep a fallback: if a tool call fails, catch the exception and return a string error
  to the model rather than crashing — the agent loop here already does this.
- Log every tool call to the terminal (already wired up) so you can debug live.
- Time-box yourself: get an ugly end-to-end demo working before polishing anything.
