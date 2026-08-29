"""
Web search tool. Uses duckduckgo-search so no API key is needed out of the box.
Swap in SerpAPI/Tavily/Google CSE here if you have a key and want better results.
"""

SCHEMA = {
    "name": "web_search",
    "description": "Search the web for current information. Returns a list of results with titles, snippets, and URLs.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query"},
            "max_results": {
                "type": "integer",
                "description": "Number of results to return (default 5)",
            },
        },
        "required": ["query"],
    },
}


def run(query: str, max_results: int = 5) -> str:
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. {r.get('title', 'No title')}\n"
                f"   {r.get('body', '')}\n"
                f"   URL: {r.get('href', '')}"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Search failed: {e}"
