#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from pprint import pprint

def cleanRssFeedElement(rss):
	feed = rss['feed']

	if "author" not in feed:
		feed['author'] = ""
	if "author_detail" not in feed:
		feed['author_detail'] = ""
	if "authors" not in feed:
		feed['authors'] = ""
	if "docs" not in feed:
		feed['docs'] = ""
	if "generator" not in feed:
		feed['generator'] = ""
	if "generator_detail" not in feed:
		feed['generator_detail'] = ""
	if "language" not in feed:
		feed['language'] = ""
	if "link" not in feed:
		feed['link'] = ""
	if "links" not in feed:
		feed['links'] = ""
	if "published" not in feed:
		feed['published'] = ""
	if "subtitle" not in feed:
		feed['subtitle'] = ""
	if "subtitle_detail" not in feed:
		feed['subtitle_detail'] = ""
	if "title" not in feed:
		feed['title'] = ""
	if "title_detail" not in feed:
		feed['title_detail'] = ""
	if "updated" not in feed:
		feed['updated'] = ""

	rss['feed'] = feed

	return rss
