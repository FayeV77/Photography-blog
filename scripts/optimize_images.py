"""Optimize raster images in place before a production build.

SVG assets and images smaller than the requested size are left untouched.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "content" / "images"
RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_WIDTH = 1920


def optimize(path: Path, write: bool) -> str:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source)
        if image.width > MAX_WIDTH:
            height = round(image.height * MAX_WIDTH / image.width)
            image = image.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)
        if not write:
            return f"CHECK {path.relative_to(ROOT)}: {image.width}x{image.height}"
        if path.suffix.lower() in {".jpg", ".jpeg"}:
            image.convert("RGB").save(path, quality=86, optimize=True, progressive=True)
        elif path.suffix.lower() == ".png":
            image.save(path, optimize=True)
        else:
            image.save(path, quality=84, method=6)
    return f"OPTIMIZED {path.relative_to(ROOT)}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write optimized raster images in place.")
    args = parser.parse_args()
    for path in sorted(IMAGE_ROOT.rglob("*")):
        if path.is_file() and path.suffix.lower() in RASTER_EXTENSIONS:
            print(optimize(path, args.write))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
