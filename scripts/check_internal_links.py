"""Fail if generated HTML contains broken root-relative internal links."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def exists_for_url(output: Path, current_file: Path, raw_url: str) -> bool:
    parsed = urlparse(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("#", "mailto:", "tel:")):
        return True
    path = parsed.path
    if not path:
        return True
    candidate = output / path.lstrip("/") if path.startswith("/") else current_file.parent / path
    return candidate.is_file() or (candidate / "index.html").is_file()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="output")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    broken: list[str] = []
    for html_file in output.rglob("*.html"):
        if "drafts" in html_file.parts:
            continue
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        for node in soup.select("a[href], img[src], link[href], script[src]"):
            if node.name == "link" and "canonical" in node.get("rel", []):
                continue
            value = node.get("href") or node.get("src")
            if value and not exists_for_url(output, html_file, value):
                broken.append(f"{html_file.relative_to(output)} -> {value}")
    if broken:
        print("Broken internal links:\n" + "\n".join(broken))
        return 1
    print("No broken root-relative internal links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
