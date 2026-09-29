from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_theme_files_exist() -> None:
    expected = [
        "theme/templates/base.html",
        "theme/templates/index.html",
        "theme/templates/article.html",
        "theme/static/css/layout.css",
        ".pages.yml",
    ]
    for path in expected:
        assert (ROOT / path).is_file(), path
