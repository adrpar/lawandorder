#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from dateutil import parser
import rssToDB as db
from pprint import pprint

from readability.readability import Document
import urllib
from bs4 import BeautifulSoup

import rssCleaner

def readRSS(url, dbConnect):
	rss = feedparser.parse(url)
	rss = rssCleaner.cleanRssFeedElement(rss)

	dbConnect.writeFeedInfo(rss['feed'])

	if dbConnect.table_id == -1:
		raise RuntimeException("Error in writing feed to DB")

	for entry in rss['entries']:
		article_id = dbConnect.writeArticleDescription(entry, dbConnect.table_id)

		#read the page
		html = urllib.urlopen(entry['link']).read()
		pageTitle = Document(html).short_title()
		soup = BeautifulSoup(Document(html).summary())
		pageContent = soup.get_text()

		dbConnect.writeArticle(entry, dbConnect.table_id, article_id, pageTitle, pageContent)



	print("Finished parsing the feed")



    


if __name__ == "__main__":
    url = "http://www.berlin.de/polizei/presse-fahndung/_rss_presse.xml"
    #url = "www.berlin.de/polizei/polizeimeldungen/index.php/rss"
    
    conn = db.rssToDB("localhost", 3306, "root", "lawandorder")
    conn.openDBConnection("mastr0")

    readRSS(url, conn)
