#!/usr/bin/env python3
import os
import json
import glob
import frontmatter
from markdown_it import MarkdownIt

# Settings
INPUT_DIR = "."
PATTERN = "**/*.md"
ESCAPE_SLASHES = True

md = MarkdownIt("commonmark")

def escape_slashes(text: str) -> str:
    return text.replace("/", "\\/") if ESCAPE_SLASHES else text

def process_markdown_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    title = post.get("title", "")
    html = md.render(post.content)

    out_obj = {"title": title, "content": html}
    json_str = json.dumps(out_obj, ensure_ascii=False)

    if ESCAPE_SLASHES:
        json_str = escape_slashes(json_str)

    base, _ = os.path.splitext(path)
#    out_path = base + ".json"
    out_path = base

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json_str)

    print(f"Wrote {out_path}")

def main():
    files = glob.glob(os.path.join(INPUT_DIR, PATTERN), recursive=True)
    if not files:
        print("No markdown files found.")
        return
    for f in files:
        process_markdown_file(f)

if __name__ == "__main__":
    main()


