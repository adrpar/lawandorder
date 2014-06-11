#!/usr/bin/env python

import sys
from warnings import filterwarnings
import feedparser
from dateutil import parser
from datetime import datetime
import MySQLdb
from pprint import pprint

#turn off warnings from MySQLdb
filterwarnings('ignore', category = MySQLdb.Warning)

class rssToDB:
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

	def writeFeedInfo(self, feed):
		#check if feed exists
		cur = self.dbConnect.cursor()

		cur.execute("SELECT feed_id FROM rssTables WHERE link=%s AND title=%s", [feed['link'], feed['title']])
		res = cur.fetchall()

		if(len(res) != 0):
			#we need to update this! but for the moment we just ignore this and set the table id
			self.table_id = res[0][0]
			cur.close()
			return

		cur.execute("""INSERT INTO rssTables 
										(author,
										 author_detail,
										 authors,
										 docs,
										 generator,
										 generator_detail,
										 language,
										 link,
										 links,
										 published,
										 subtitle,
										 subtitle_detail,
										 title,
										 title_detail,
										 updated)
									VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
						[feed['author'], 
						 feed['author_detail'],
						 feed['authors'],
						 feed['docs'],
						 feed['generator'],
						 feed['generator_detail'],
						 feed['language'],
						 feed['link'],
						 feed['links'],
						 parser.parse(feed['published']),
						 feed['subtitle'],
						 feed['subtitle_detail'],
						 feed['title'],
						 feed['title_detail'],
						 parser.parse(feed['updated']),
						 ])

		#get the current table_id
		cur = self.dbConnect.cursor()
		cur.execute("SELECT feed_id FROM rssTables WHERE link=%s AND title=%s", [feed['link'], feed['title']])

		res = cur.fetchone()
		self.table_id = res[0]

		cur.close()

		self.dbConnect.commit()

	def writeArticleDescription(self, article, feed_id):
		#check if feed exists
		cur = self.dbConnect.cursor()

		cur.execute("SELECT articleDesc_id FROM rssArticlesDescription WHERE link=%s AND title=%s", [article['link'], article['title']])
		res = cur.fetchall()

		if(len(res) != 0):
			article_id = res[0]

			cur.close()
			return article_id

		cur.execute("""INSERT INTO rssArticlesDescription 
										(feed_id,
											id,
											author,
											author_detail,
											authors,
											link,
											links,
											title,
											title_detail,
											summary,
											published,
											guidislink)
									VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
						[feed_id, 
						 article['id'],
						 article['author'],
						 article['author_detail'],
						 article['authors'],
						 article['link'],
						 article['links'],
						 article['title'],
						 article['title_detail'],
						 article['summary'],
						 parser.parse(article['published']),
						 article['guidislink'],
						 ])

		#get the current table_id
		cur = self.dbConnect.cursor()
		cur.execute("SELECT articleDesc_id FROM rssArticlesDescription WHERE link=%s AND title=%s", [article['link'], article['title']])

		res = cur.fetchone()
		article_id = res[0]

		cur.close()

		self.dbConnect.commit()

		return article_id

	def writeArticle(self, article, feed_id, articleDesc_id, parsedTitle, content):
		#check if feed exists
		cur = self.dbConnect.cursor()

		cur.execute("SELECT article_id FROM rssArticles WHERE link=%s AND rssTitle=%s", [article['link'], article['title']])
		res = cur.fetchall()

		if(len(res) != 0):
			cur.close()
			return

		cur.execute("""INSERT INTO rssArticles 
										(articleDesc_id,
											feed_id,
											link,
											parseDate,
											rssTitle,
											parsedTitle,
											content)
									VALUES ( %s, %s, %s, %s, %s, %s, %s )""",
						[articleDesc_id, 
						 feed_id,
						 article['link'],
						 parser.parse(datetime.today().isoformat(' ')),
						 article['title'],
						 parsedTitle,
						 content,
						 ])

		cur.close()

		self.dbConnect.commit()

	def fetchAllArticles(self):
		#get all articles
		cur = self.dbConnect.cursor()

		cur.execute("SELECT * FROM rssArticles")
		res = cur.fetchall()

		return res

	def fetchAllArticlesDescriptions(self):
		#get all articles
		cur = self.dbConnect.cursor()

		cur.execute("SELECT * FROM rssArticlesDescription")
		res = cur.fetchall()

		return res
