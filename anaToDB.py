#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from warnings import filterwarnings
import MySQLdb
from pprint import pprint
import json

#turn off warnings from MySQLdb
filterwarnings('ignore', category = MySQLdb.Warning)

class anaToDB:
	def __init__(self, host, port, user, db):
		self.host = host
		self.port = port
		self.user = user
		self.db = db

		self.table_id = -1

	def openDBConnection(self, pwd):
		self.dbConnect = MySQLdb.connect(host=self.host,
								port=self.port,
								user=self.user,
								passwd=pwd,
								db=self.db,
								charset='utf8',
                    			use_unicode=True)	

	def articleAlreadyProcessed(self, id):
		cur = self.dbConnect.cursor()

		cur.execute("SELECT * FROM articlesAnaSum WHERE article_id = %s limit 1", [id])
		res = cur.fetchall()

		if(len(res) == 0):
			return False
		else:
			return True

	def writeArticlesAna(self, article_id, NERTags):
		if(self.articleAlreadyProcessed(article_id)):
			return

		#reconfigure tags
		NERTagsNew = [ word for x in NERTags for word in x ]

		NERTagsString = json.dumps(NERTagsNew, ensure_ascii=False, encoding='utf8')

		cur = self.dbConnect.cursor()

		cur.execute("""INSERT INTO articlesAnaSum
										(article_id,
										 NERTags)
								VALUES ( %s, %s, %s )""",
						[article_id,
						 NERTagsString
					])

		#get the current articlesAnaSum_id
		cur = self.dbConnect.cursor()
		cur.execute("SELECT articlesAnaSum_id FROM articlesAnaSum WHERE article_id=%s", [article_id])

		res = cur.fetchone()
		articlesAnaSum_id = res[0]

		cur.close()

		self.dbConnect.commit()

		self.writeWords(articlesAnaSum_id, NERTagsNew)

	def writeWords(self, articlesAnaSum_id, NERTags):
		cur = self.dbConnect.cursor()

		for word in NERTags:
			cur.execute("""INSERT INTO words 
											(articlesAnaSum_id,
											 word,
											 NERTag)
									VALUES ( %s, %s, %s )""",
							[articlesAnaSum_id,
							 word[0],
							 word[1],
						])

		cur.close()

		self.dbConnect.commit()

	def articleLocationAlreadyProcessed(self, id, table):
		cur = self.dbConnect.cursor()

		cur.execute("SELECT * FROM " + table + " WHERE article_id = %s limit 1", [id])
		res = cur.fetchall()

		if(len(res) == 0):
			return False
		else:
			return True

	def writeArticleLocation(self, table, article, articleDesc, locationText, location):
		if(self.articleLocationAlreadyProcessed(article[0], table)):
			return

		cur = self.dbConnect.cursor()

		cur.execute("""INSERT INTO """ + table + """
										(article_id,
										 locationText,
										 locationJson,
										 articleTitle,
										 published,
										 lon,
										 lat)
								VALUES ( %s, %s, %s, %s, %s, %s, %s )""",
						[article[0],
						 locationText,
						 json.dumps(location),
						 article[5],
						 articleDesc[11],
						 location['lon'],
						 location['lat']
					])

		cur.close()

		self.dbConnect.commit()

	def fetchAllArticleLocations(self, table):
		#get all articles
		cur = self.dbConnect.cursor()

		cur.execute("SELECT * FROM " + table)
		res = cur.fetchall()

		return res

