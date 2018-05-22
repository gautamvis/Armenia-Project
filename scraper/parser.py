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

	def __init__(self, url, title, body):

		self.url = url
		self.title = title
		self.body = body


# Thread function takes in URL and collects article data
def parseArticlesArmenpress(article_urls):

	parsed_articles = []

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
			
			#TODO: parse other info

			#Add to result list
			parsed_articles.append(ArticleData(url, title, body))

		except Exception as e:
			print e
			pass

	return parsed_articles

	
if __name__ == "__main__":


	#Load URL list from pickle file
	with open("article_urls.pkl", 'rb') as pkl_file:
		article_urls = pickle.load(pkl_file)

	#Parse each article
	parsed_articles = parseArticlesArmenpress(article_urls)

	#Write info to CSV file
	with open('article_data.csv', 'wb') as outfile:
			
		writer = csv.writer(outfile)
		writer.writerow(['title', 'summary'])

		for article in parsed_articles:
			writer.writerow([article.title, article.body])


	#TODO thread to improve speed

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
	

	#TODO: Print metrics for dataset

   
