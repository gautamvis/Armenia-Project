# Parser for Armenia Project
# Gautam Visveswaran, May 2018

import errno, json, os, pickle, re, shutil, string, sys, unicodedata, time, math
import unicodecsv as csv
from requests import get
from bs4 import *
from threading import Thread
from selenium import webdriver


#Object to store data for each article
class ArticleData():

	def __init__(self, url, title, date, body, summary):

		self.url = url
		self.title = title
		self.date = date
		self.body = body
		self.summary = summary
		


# Thread function takes in URL and collects article data
def parseArticlesArmenpress(article_urls, outfile):

	parsed_articles = []

	with open(csv_file, 'wb') as outfile:
		
		writer = csv.writer(outfile)


		for url in article_urls:

			try:
				#Get the article 
				article_html = get(url)
		
				#Parse with beautifulsoup
				article_soup = BeautifulSoup(article_html.text, "html.parser")

				#Find title and body of each article
				title = article_soup.find(class_="opennewstitle").contents[0]
				body = article_soup.find(itemprop="articleBody").contents[0]
				#Remove HTML tags and special characters
				title = re.sub(re.compile('<.*?>'), '', title.encode('utf-8'))
				title = re.sub('[^ a-zA-Z0-9]', '', title)
				body = re.sub(re.compile('<.*?>'), '', body.encode('utf-8'))
				body = re.sub('[^ a-zA-Z0-9]', '', body)
				

				#Add to result list
				parsed_articles.append(ArticleData(url, title, body))



			except Exception as e:
				print e
				pass

	return parsed_articles


def parseArticlesRFERL(article_urls, outfile):

	parsed_articles = []

	with open(csv_file, 'wb') as outfile:
		
		writer = csv.writer(outfile)


		for url in article_urls:
		# for i in range(0,10):

			try:

				#Get the article 
				article_html = get(url)
				# article_html = get(article_urls[i])
		
				#Parse with beautifulsoup
				article_soup = BeautifulSoup(article_html.text, "html.parser")



				#Get content and title
				body = article_soup.find(class_="wsw").contents[0]
				title = article_soup.find(class_="pg-title").contents[0]
				date = str(article_soup.find("time").contents[0].strip())
				summary = str(article_soup.find(True, {'class':['intro', 'content-offset']}).find(class_="wsw").text)


				title = re.sub(re.compile('<.*?>'), '', title.encode('utf-8'))
				title = re.sub('[^ a-zA-Z0-9]', '', title)
				body = re.sub(re.compile('<.*?>'), '', body.encode('utf-8'))
				body = re.sub('[^ a-zA-Z0-9]', '', body)
				summary = re.sub(re.compile('<.*?>'), '', summary.encode('utf-8'))
				summary = re.sub('[^ a-zA-Z0-9]', '', summary)


				article = ArticleData(url, title, date, body, summary)
				parsed_articles.append(article)
				writer.writerow([article.url, article.title, article.date, article.body, article.summary])
				# parsed_articles.append(ArticleData(article_urls[i], title, date, body, summary))

				

			except Exception as e:
				print e
				pass

	return parsed_articles

	
if __name__ == "__main__":

	website = sys.argv[1]
	article_pkl = sys.argv[2]
	csv_file = sys.argv[3]

	#Load URL list from pickle file
	with open(article_pkl, 'rb') as pkl_file:
		article_urls = pickle.load(pkl_file)

	#Parse each article
	if website.lower() == "armenpress":
		parsed_articles = parseArticlesArmenpress(article_urls)
	elif website.lower() == "rferl":
		parsed_articles = parseArticlesRFERL(article_urls, csv_file)


			


	#TODO thread to improve speed?

	#Create a thread to crawl each url, store in thread_pool list
	# for url in urls:
	#   try:
	#       thread = Thread(target = parseSoupArmenpress, args = (url,))
	#       thread_pool.append(thread)
	#   except: 
	#       pass

	# Start all threads
	# for thread in thread_pool:
	#   thread.start()

	# Join all threads
	# for thread in thread_pool:
	#   thread.join()
	

   
