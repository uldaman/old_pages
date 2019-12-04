#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import bulrush

THEME = bulrush.PATH
JINJA_ENVIRONMENT = bulrush.ENVIRONMENT
JINJA_FILTERS = bulrush.FILTERS

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets']

AUTHOR = u'HanXiao'
SITENAME = 'Small Cpp'
SITEURL = 'http://www.smallcpp.cn'
PATH = 'content'
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh'
GITHUB_URL = 'https://github.com/uldaman'
SITESUBTITLE = u'勿在浮沙筑高台, 练从难处练, 用从易处用.'

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_RSS = None
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None

# LINKS widget
LINKS = (
    ('Learning Notes', 'https://zhuec.gitbook.io/learning-notes/'),
    ('VeChain Thor', 'https://github.com/vechain/thor'),
    ('CSDN', 'http://blog.csdn.net/u010850265'),
)

DEFAULT_PAGINATION = False  # 不分页

USE_FOLDER_AS_CATEGORY = True  # 这个可以让 pelican 根据 content 里的文件夹结构自动生成文章分类

DELETE_OUTPUT_DIRECTORY = True  # 编译之前删除 output 目录，这样保证 output 下生成的内容干净

SUMMARY_MAX_LENGTH = 25  # 文章摘要最大字数

MARKDOWN = {
    'extension_configs': {
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {},
        "markdown.extensions.headerid": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.sane_lists": {},
        "markdown.extensions.smarty": {},
        "markdown.extensions.wikilinks": {},
        "markdown.extensions.admonition": {},
        "markdown.extensions.codehilite": {"guess_lang": False, "pygments_style": "perldoc", "noclasses": True},
    },
    'output_format': 'html5',
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
