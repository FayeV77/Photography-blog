"""Validate article metadata and the one-admin configuration before a production build."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "content" / "articles"
IMAGES_DIR = ROOT / "content" / "images"
ADMIN_FILE = ROOT / "data" / "admin.yml"
REQUIRED_ARTICLE_FIELDS = {"title", "slug", "date", "author", "category", "summary", "cover", "cover_alt", "status"}
VALID_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER = "REPLACE_WITH_GITHUB_USERNAME"


def read_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter opening delimiter")
    try:
        _, header, body = text.split("---\n", 2)
    except ValueError as error:
        raise ValueError("missing YAML front matter closing delimiter") from error
    metadata = yaml.safe_load(header) or {}
    if not isinstance(metadata, dict):
        raise ValueError("front matter must be a YAML mapping")
    return metadata, body


def validate_admin(errors: list[str], allow_placeholder: bool) -> None:
    if not ADMIN_FILE.exists():
        errors.append("data/admin.yml is missing")
        return
    try:
        config = yaml.safe_load(ADMIN_FILE.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        errors.append(f"data/admin.yml is invalid YAML: {error}")
        return
    admin = config.get("admin")
    if config.get("single_admin") is not True or not isinstance(admin, dict):
        errors.append("data/admin.yml must contain single_admin: true and exactly one admin mapping")
        return
    username = str(admin.get("github_username", "")).strip()
    if not username:
        errors.append("admin.github_username is required")
    elif username == PLACEHOLDER and not allow_placeholder:
        errors.append("admin.github_username still uses the placeholder; replace it before production deploy")
    if admin.get("active") is not True:
        errors.append("admin account must be active")
    expected_permissions = {"create_post", "edit_post", "delete_post", "publish_post", "manage_media"}
    if set(admin.get("permissions", [])) != expected_permissions:
        errors.append("admin permissions must match the single-admin policy")


def validate_article(path: Path, seen_slugs: set[str], errors: list[str], warnings: list[str]) -> None:
    try:
        metadata, body = read_front_matter(path)
    except (ValueError, yaml.YAMLError) as error:
        errors.append(f"{path.relative_to(ROOT)}: {error}")
        return
    missing = sorted(field for field in REQUIRED_ARTICLE_FIELDS if not metadata.get(field))
    if missing:
        errors.append(f"{path.relative_to(ROOT)}: missing required field(s): {', '.join(missing)}")
        return
    slug = str(metadata["slug"])
    if not VALID_SLUG.fullmatch(slug):
        errors.append(f"{path.relative_to(ROOT)}: invalid slug '{slug}'")
    if slug in seen_slugs:
        errors.append(f"{path.relative_to(ROOT)}: duplicate slug '{slug}'")
    seen_slugs.add(slug)
    if metadata["status"] not in {"draft", "published"}:
        errors.append(f"{path.relative_to(ROOT)}: status must be draft or published")
    cover = str(metadata["cover"]).lstrip("/")
    if not (ROOT / "content" / cover).is_file():
        errors.append(f"{path.relative_to(ROOT)}: cover image not found: {cover}")
    if len(str(metadata["summary"])) < 20:
        warnings.append(f"{path.relative_to(ROOT)}: summary is shorter than 20 characters")
    if "## " not in body and metadata["status"] == "published":
        warnings.append(f"{path.relative_to(ROOT)}: published article has no H2 heading")
    for image_alt in re.findall(r"!\[([^\]]*)\]\([^)]*\)", body):
        if not image_alt.strip():
            warnings.append(f"{path.relative_to(ROOT)}: image in article body has empty alt text")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-placeholder-admin", action="store_true", help="Only for local demo builds before the owner sets a GitHub username.")
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    validate_admin(errors, args.allow_placeholder_admin)
    seen_slugs: set[str] = set()
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        validate_article(path, seen_slugs, errors, warnings)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(seen_slugs)} article(s) and the single-admin configuration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
