from __future__ import annotations
from . import schemas
from pathlib import Path
import os
import json
import datetime

# wrapper handlers expected to return a JSON string

def _get_ai_brain_root(task: dict) -> Path:
    out = task.get("out_root") or os.environ.get("AI_BRAIN_PATH")
    if out:
        return Path(out)
    # default to known mount path (user's AI_Brain)
    return Path("/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain")


def _save_result(path: Path, summary: str):
    return json.dumps({"status": "ok", "path": str(path), "summary": summary}, ensure_ascii=False)


def collect_content(args: dict, **kwargs) -> str:
    """Accept raw HTML/text and save as cleaned markdown using existing utils."""
    from .utils.cleaner import clean_html_to_markdown
    content = args.get("content")
    title = args.get("title")
    url = args.get("url")
    if not content or not title:
        return json.dumps({"status": "error", "error": "missing content or title"})

    root = _get_ai_brain_root(args)
    out_dir = root / "raw" / "articles"
    out_dir.mkdir(parents=True, exist_ok=True)

    cleaned = clean_html_to_markdown(content)
    # reuse existing save logic from collector_core if available
    try:
        from .collector_core import save_article
        saved = save_article(cleaned, url or "", title, [], output_dir=str(out_dir))
        return _save_result(Path(saved), cleaned[:200])
    except Exception:
        # fallback: write minimal markdown
        fname = out_dir / f"{datetime.now().strftime('%Y-%m-%d')}_{title.replace(' ','_')}.md"
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return _save_result(fname, cleaned[:200])


def collect_url(args: dict, **kwargs) -> str:
    """Fetch a URL (requests) and save cleaned markdown."""
    import requests
    url = args.get("url")
    if not url:
        return json.dumps({"status":"error","error":"missing url"})

    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        return json.dumps({"status":"error","error":f"http {resp.status_code}"})
    content = resp.text
    title = args.get("title") or url
    return collect_content({"content": content, "title": title, "url": url, "out_root": args.get("out_root")})
