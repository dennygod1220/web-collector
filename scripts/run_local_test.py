#!/usr/bin/env python3
"""Smoke test for web-collector plugin core modules."""
import sys
from pathlib import Path

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

# Test 1: cleaner.py
from utils.cleaner import clean_html_to_markdown
html = "<html><script>evil</script><body><p>Hello World</p></body></html>"
cleaned = clean_html_to_markdown(html)
assert "evil" not in cleaned
assert "Hello World" in cleaned
print(f"[PASS] utils/cleaner.py — removed script, extracted content")

# Test 2: collector_core.py
from collector_core import save_article
import tempfile, os

with tempfile.TemporaryDirectory() as tmpdir:
    path = save_article(
        content="Test content",
        url="https://example.com",
        title="Smoke Test",
        tags=["test"],
        output_dir=tmpdir
    )
    assert os.path.exists(path)
    content = Path(path).read_text()
    assert "---" in content
    assert "source: https://example.com" in content
    assert "title: Smoke Test" in content
    print(f"[PASS] collector_core.py — frontmatter + content correct, saved to {path}")

print("\n✅ All smoke tests passed (tools.py requires Hermes runtime)")
