import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pelicanconf import *  # noqa: F403

SITEURL = os.environ.get("SITEURL", "")
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
DRAFT_URL = ""
DRAFT_SAVE_AS = ""

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
