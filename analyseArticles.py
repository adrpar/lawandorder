#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import nltk
import anaToDB as anaDb
import rssToDB as rssDb
from pprint import pprint

def analyseArticles(anaDbConnect, rssDbConnect):
	articles = rssDbConnect.fetchAllArticles()

	sentencesParser = nltk.data.load('tokenizers/punkt/german.pickle')
	NERTagger = nltk.tag.stanford.NERTagger('/Users/adrian/Documents/Development/lawandorder/data/ner-model.ser.gz', '/opt/stanford-ner/stanford-ner.jar', encoding="utf8")

	#go through all articles and do some basic text analysis
	for article in articles:
		#first see, if we have already processed this
		if(anaDbConnect.articleAlreadyProcessed(article[0]) == 0):
			#get all sentences from the article
			print article[0]
			sentences = sentencesParser.tokenize(article[7])

			sentenceTags = []
			NERTags = []

			for x in sentences:
				sentenceTags = sentenceTags + [ x.split() ]

			NERTags = NERTags + NERTagger.batch_tag(sentenceTags)

			anaDbConnect.writeArticlesAna(article[0], NERTags)

	print("Finished analysing everything")



    


if __name__ == "__main__":
    connRss = rssDb.rssToDB("localhost", 3306, "root", "lawandorder")
    connAna = anaDb.anaToDB("localhost", 3306, "root", "lawandorder")
    connRss.openDBConnection("mastr0")
    connAna.openDBConnection("mastr0")

    analyseArticles(connAna, connRss)
