COLLECT_URL = {
    "name": "collect_url",
    "description": "Fetch a URL and save cleaned Markdown into AI_Brain/raw/articles. Returns {path, summary}.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "The URL to fetch"},
            "out_root": {"type": "string", "description": "Optional: AI_BRAIN_PATH override"}
        },
        "required": ["url"]
    }
}

COLLECT_CONTENT = {
    "name": "collect_content",
    "description": "Accept raw HTML/text and save cleaned Markdown into AI_Brain/raw/articles. Returns {path, summary}.",
    "parameters": {
        "type": "object",
    "properties": {
        "content": {"type": "string", "description": "Raw HTML or text content"},
        "title": {"type": "string", "description": "Title to use for file"},
        "url": {"type": "string", "description": "Source URL (optional)"},
        "out_root": {"type": "string", "description": "Optional: AI_BRAIN_PATH override"}
    },
    "required": ["content", "title"]
    }
}
