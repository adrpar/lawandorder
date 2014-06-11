#!/usr/bin/env python

import sys
import json
import anaToDB as anaDb
import rssToDB as rssDb
import re
import requests, urllib
from pprint import pprint

def analyseLocation(anaDbConnect, rssDbConnect):
	articles = rssDbConnect.fetchAllArticles()
	articlesDesc = rssDbConnect.fetchAllArticlesDescriptions()

	streetRegex = re.compile(u'(\w+stra(ss|\u00DF)e)', re.U)
	StreetRegex = re.compile(u'(\w+\sStra(ss|\u00DF)e)', re.U)

	#go through all articles and do some basic text analysis
	for article, articleDesc in zip(articles, articlesDesc):
		#first see, if we have already processed this
		if(anaDbConnect.articleLocationAlreadyProcessed(article[0], "simpleAnaLocations") == 0):
			#obtain street with simple regex - if no street given, set location to "BERLIN"
			streets = streetRegex.search(unicode(article[7]))
			Streets = StreetRegex.search(unicode(article[7]))

			if streets:
				street = streets.groups()[0]
			elif Streets:
				street = Streets.groups()[0]
			else:
				continue

			street = street + u" Berlin"

			query = requests.get("http://nominatim.openstreetmap.org/search", params={"format": "json", 
																						"limit": 1, 
																						"q": street})
			location = json.loads(query.text)

			if not location:
				continue

			print(street)

			anaDbConnect.writeArticleLocation("simpleAnaLocations", article, articleDesc, street, location[0])

	print("Finished analysing everything")


def jsonLocationSummary(anaDbConnect, rssDbConnect):
	articleLocations = anaDbConnect.fetchAllArticleLocations("simpleAnaLocations")
	
	results = []

	for articleLocation in articleLocations:
		result = { "id": articleLocation[1],
					"title": articleLocation[4],
					"time": articleLocation[5].isoformat(),
					"lon": articleLocation[6],
					"lat": articleLocation[7]
				 }

		results.append(result)

	print(json.dumps(results))

def jsonArticles(anaDbConnect, rssDbConnect):
	articles = rssDbConnect.fetchAllArticles()

	results = []
	
	for article in articles:
		result = { "id": article[1],
					"link": article[3],
					"title": article[5],
					"text": article[7],
				 }

		results.append(result)

	print(json.dumps(results))


if __name__ == "__main__":
    connRss = rssDb.rssToDB("localhost", 3306, "root", "lawandorder")
    connAna = anaDb.anaToDB("localhost", 3306, "root", "lawandorder")
    connRss.openDBConnection("mastr0")
    connAna.openDBConnection("mastr0")

    #analyseLocation(connAna, connRss)
    #jsonLocationSummary(connAna, connRss)
    jsonArticles(connAna, connRss)
