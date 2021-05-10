#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# from __future__ import unicode_literals
import os
import codecs
import sys
sys.path.append(os.curdir)

from patreonconf import *

import logging

# Path for content
PATH = 'content'

# Basic settings
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = "Unsorted"

# Smart quotes and other things
TYPOGRIFY = True

# Stop putting &nbsp; in the article titles
TYPOGRIFY_IGNORE_TAGS = [
    'pre', 'code', 'header', 'h1', 'h2', 'h3', 'aside',
]

# Directory behavior
PATH = 'content/'
PAGE_PATHS = ['pages/']
PATH_METADATA = 'pages/(?P<fullpath>.+)[.].+'
STATIC_PATHS = [
    'favicon.png', 
    'robots.txt',
    'media/',
]

# Static pages from theme
TEMPLATE_PAGES = {
    # unused
}

# Search is from the Tipue plugin
DIRECT_TEMPLATES = [
    'index', 'categories', 'tags', 'archives', 
    # 'search'
]

# Don't process HTML files
READERS = dict(html=None)

# Article url schema
INDEX_SAVE_AS = 'index.html'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'

TAG_URL = 'tag/{slug}/'
TAGS_SAVE_AS = 'tag/index.html'
TAGS_URL = 'tag/index.html'
TAG_SAVE_AS = 'tag/{slug}/index.html'

ARCHIVES_URL = 'posts/'
ARCHIVES_SAVE_AS = 'posts/index.html'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/index.html'

CATEGORY_URL = 'category/{slug}/index.html'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_URL = 'tag/{slug}/index.html'
TAG_SAVE_AS = 'tag/{slug}/index.html'

CATEGORIES_SAVE_AS = "category/index.html"
AUTHORS_SAVE_AS = "author/index.html"

# Page url schema
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Octopress-compatible filename metadata parsing
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Theme and theme settings
THEME = "localtheme"

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 4
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Jinja config

def sort_by_article_count(tags):
    return sorted(tags, key=lambda pairs: len(pairs[1]), reverse=True)


JINJA_FILTERS = {
    "sort_by_article_count": sort_by_article_count,
}

JINJA_ENVIRONMENT = {
    "trim_blocks": True,
    "lstrip_blocks": True,
    "extensions": ["jinja2_time.TimeExtension"]
}

# Plugins

PLUGIN_PATHS = ["pelican-plugins", "local-plugins", "."]
PLUGINS = [
    'patreonjson',
    'summary',
    'sex_vampires',
    'renderdeps',
    'anchorlinks',
    'htmlval',
    'neighbors',
]

# Plugin config for summary
SUMMARY_BEGIN_MARKER = '<!-- startsummary -->'
SUMMARY_END_MARKER = '<!-- more -->'  # octopress compat
# Require an explicit summary declaration, don't auto-summarize.
SUMMARY_MAX_LENGTH = None

# Plugin config for custom article urls
# Preserve the old blog URL for blog stuff
# This is all really unnecessary given the URL options built in to pelican now.
# CUSTOM_ARTICLE_URLS = {
#     'blog': dict(
#         URL='{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/',
#         SAVE_AS='{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html',
#     ),
# }

RENDER_DEPS = [
    (
        (["pre"], {"class_": "markdeep"}), 
        """<script>window.markdeepOptions={mode:"html"};</script>
<style class="fallback">pre.markdeep{white-space:pre;font-family:monospace}</style>
<script src="https://casual-effects.com/markdeep/latest/markdeep.min.js"></script>"""),
    (
        (["pre"], {"class_": "mermaid"}), 
        # '<script src="https://unpkg.com/mermaid@8.8.0/dist/mermaid.min.js"></script>'
        '<script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>'
    ),
    (
        (["blockquote"], {"class_": "twitter-tweet"}), 
        # '<script async="true" src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'  # too slow
        '<link href="/theme/css/twitter.css" rel="stylesheet" type="text/css" defer>'
    ),
    (
        ([], {"class_": "critic"}), 
        '<link href="/theme/css/critic.css" rel="stylesheet" type="text/css" defer>'
    ),
    (
        (["kbd"], {}), 
        '<link href="/theme/css/keyboard.css" rel="stylesheet" type="text/css" defer>'
    )
]
