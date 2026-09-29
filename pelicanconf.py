from pathlib import Path
import re

import yaml
from jinja2 import pass_context
from markupsafe import Markup

PROJECT_ROOT = Path(__file__).parent
with (PROJECT_ROOT / "data" / "site.yml").open(encoding="utf-8") as site_file:
    SITE = yaml.safe_load(site_file)

AUTHOR = SITE["author"]
SITENAME = SITE["site_name"]
SITEURL = ""
SITESUBTITLE = SITE["tagline"]
SITE_DESCRIPTION = SITE["description"]
SITE_BACKGROUND = SITE["background_image"]
SITE_COPYRIGHT = SITE["copyright"]


@pass_context
def with_site_url(context, html: str) -> Markup:
    """Make CMS root-relative media paths work on GitHub project pages.

    Pages CMS writes inserted images as /images/..., while a GitHub project
    page is served below a repository path such as /learn-cine/. The filter
    injects SITEURL during production builds and leaves local preview paths
    untouched.
    """

    site_url = str(context.get("SITEURL", "")).rstrip("/")
    if not site_url:
        return Markup(html)
    rewritten = re.sub(
        r'(?P<attribute>\b(?:src|href)=["\'])/images/',
        rf'\g<attribute>{site_url}/images/',
        str(html),
    )
    return Markup(rewritten)

PATH = "content"
TIMEZONE = "Asia/Ho_Chi_Minh"
DEFAULT_LANG = "vi"
DEFAULT_DATE_FORMAT = "%d/%m/%Y"

ARTICLE_URL = "blog/{slug}/"
ARTICLE_SAVE_AS = "blog/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"

ARTICLE_ORDER_BY = "reversed-date"
DEFAULT_PAGINATION = 9
PAGINATION_PATTERNS = ((1, "{base_name}/", "{base_name}/index.html"), (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"))

THEME = "theme"
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "images/favicon.svg": {"path": "favicon.svg"},
    "extra/404.txt": {"path": "404.html"},
}

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.attr_list": {},
        "markdown.extensions.extra": {},
        "markdown.extensions.sane_lists": {},
        "markdown.extensions.toc": {"permalink": True},
    },
    "output_format": "html5",
}

PLUGINS = ["yaml_metadata"]
JINJA_FILTERS = {"with_site_url": with_site_url}
DIRECT_TEMPLATES = ["index", "categories", "tags", "archives"]
PAGINATED_TEMPLATES = {"index": None}

MENUITEMS = (
    ("Trang chủ", "/"),
    ("Bài viết", "/"),
    ("Giới thiệu", "/gioi-thieu/"),
    ("Liên hệ", "/lien-he/"),
)

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
TAG_FEED_ATOM = None

DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = True
