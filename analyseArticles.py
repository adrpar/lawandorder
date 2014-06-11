#!/usr/bin/env python

import sys
import json
import nltk
import anaToDB as anaDb
import rssToDB as rssDb
from pprint import pprint

def analyseArticles(anaDbConnect, rssDbConnect):
	articles = rssDbConnect.fetchAllArticles()

	sentencesParser = nltk.data.load('tokenizers/punkt/german.pickle')
	POSTagger = nltk.tag.stanford.POSTagger('/opt/stanford-postagger/models/german-hgc.tagger', '/opt/stanford-postagger/stanford-postagger.jar', encoding="utf8")
	NERTaggerEn = nltk.tag.stanford.NERTagger('/opt/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '/opt/stanford-ner/stanford-ner.jar', encoding="utf8")
	NERTaggerGe = nltk.tag.stanford.NERTagger('/opt/stanford-ner/classifiers/hgc_175m_600.crf.ser.gz', '/opt/stanford-ner/stanford-ner.jar', encoding="utf8")

	#go through all articles and do some basic text analysis
	for article in articles:
		#first see, if we have already processed this
		if(anaDbConnect.articleAlreadyProcessed(article[0]) == 0):
			#get all sentences from the article
			print article[0]
			sentences = sentencesParser.tokenize(article[7])

			sentenceTags = []
			POSTags = []
			NERTagsEn = []
			NERTagsGe = []

			for x in sentences:
				sentenceTags = sentenceTags + [ x.split() ]

			POSTags = POSTags + POSTagger.batch_tag(sentenceTags)
			NERTagsEn = NERTagsEn + NERTaggerEn.batch_tag(sentenceTags)
			NERTagsGe = NERTagsGe + NERTaggerGe.batch_tag(sentenceTags)

			anaDbConnect.writeArticlesAna(article[0], POSTags, NERTagsEn, NERTagsGe)

	print("Finished analysing everything")



    


if __name__ == "__main__":
    connRss = rssDb.rssToDB("localhost", 3306, "root", "lawandorder")
    connAna = anaDb.anaToDB("localhost", 3306, "root", "lawandorder")
    connRss.openDBConnection("mastr0")
    connAna.openDBConnection("mastr0")

    analyseArticles(connAna, connRss)

#author
#author_detail
#authors
#docs
#geneator
#geneator_detail
#language
#links
#links
#published
#subtitle
#subtitle_detail
#title
#title_detail
#updated



#id
#link
#links
#published
#title
#title_detail

