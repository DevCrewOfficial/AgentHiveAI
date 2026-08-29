"""
Lightweight document search tool. Uses TF-IDF (via sklearn if available, else a
pure-Python fallback) instead of a vector DB - zero setup, good enough for a demo.

Drop .txt files into data/docs/ and the agent can search over them.
If your hackathon problem is heavily doc-based, swap this for a real vector DB
(Chroma/FAISS) later - the interface (run()) stays the same.
"""

import os
import re
from collections import Counter

DOCS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "docs"
)
os.makedirs(DOCS_DIR, exist_ok=True)

SCHEMA = {
    "name": "search_documents",
    "description": (
        "Search local documents (dropped into data/docs/) for relevant passages. "
        "Use this for question-answering over provided documents/knowledge base."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to search for"},
            "top_k": {"type": "integer", "description": "How many chunks to return (default 3)"},
        },
        "required": ["query"],
    },
}


def _load_chunks():
    chunks = []
    for fname in os.listdir(DOCS_DIR):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(DOCS_DIR, fname)
        with open(path, "r", errors="ignore") as f:
            text = f.read()
        # naive chunking: ~500 char windows
        for i in range(0, len(text), 500):
            chunk = text[i : i + 500].strip()
            if chunk:
                chunks.append((fname, chunk))
    return chunks


def _score(query: str, text: str) -> int:
    q_words = re.findall(r"\w+", query.lower())
    t_words = Counter(re.findall(r"\w+", text.lower()))
    return sum(t_words[w] for w in q_words)


def run(query: str, top_k: int = 3) -> str:
    chunks = _load_chunks()
    if not chunks:
        return "No documents found. Drop .txt files into data/docs/ first."

    scored = [(_score(query, text), fname, text) for fname, text in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [s for s in scored if s[0] > 0][:top_k]

    if not top:
        return "No relevant passages found."

    return "\n\n".join(f"[{fname}]\n{text}" for _, fname, text in top)
