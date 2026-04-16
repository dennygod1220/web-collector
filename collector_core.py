import os
import yaml
from datetime import datetime
from pathlib import Path
from utils.cleaner import clean_html_to_markdown


def save_article(content: str, url: str, title: str, tags: list, output_dir: str = None):
    """
    將內容儲存為帶有 YAML Frontmatter 的 Markdown。

    Args:
        content: 清洗後的文章內容
        url: 來源網址
        title: 文章標題
        tags: 標籤列表
        output_dir: 輸出目錄，預設 AI_Brain/raw/articles/
    """
    if output_dir is None:
        # Precedence: AI_BRAIN_PATH env var > hardcoded default
        env_path = os.environ.get("AI_BRAIN_PATH")
        if env_path:
            base = Path(env_path)
        else:
            base = Path("/mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain")
        output_dir = base / "raw" / "articles"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).rstrip()
    safe_title = safe_title.replace(' ', '_')
    filename = output_dir / f"{date_str}_{safe_title}.md"

    metadata = {
        "date": date_str,
        "source": url,
        "title": title,
        "tags": tags
    }

    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.dump(metadata, allow_unicode=True, default_flow_style=False))
        f.write("---\n\n")
        f.write(content)

    return str(filename)
