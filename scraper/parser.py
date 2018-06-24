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

	def __init__(self, url, title, date, body):

		self.url = url
		self.title = title
		self.date = date
		self.body = body
		


# Thread function takes in URL and collects article data
def parseArticlesArmenpress(article_urls, outfile):

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
				article = ArticleData(url, title, date, body)
				writer.writerow([article.url, article.title, article.date, article.body])

			except Exception as e:
				print e
				pass



def parseArticlesRFERL(article_urls, outfile):


	with open(csv_file, 'wb') as outfile:
		
		writer = csv.writer(outfile)

		for url in article_urls:

			try:

				#Get the article 
				article_html = get(url)
		
				#Parse with beautifulsoup
				article_soup = BeautifulSoup(article_html.text, "html.parser")

				#Get article content
				body = article_soup.find(class_="wsw")
				if body.find(class_="wsw"):
					body.find(class_="wsw").decompose()
				if body.find("em"):
					body.find("em").decompose()
				body = body.text.strip()

				title = str(article_soup.find(class_="pg-title").contents[0])
				date = str(article_soup.find("time").contents[0].strip())
				
				header_container = article_soup.select('div.intro.content-offset')
				if header_container:
					body = str(header_container[0].text) + body

				title = ' '.join(title.split())
				body = ' '.join(body.split())

				article = ArticleData(url, title, date, body)
				writer.writerow([article.url, article.title, article.date, article.body])

			except Exception as e:
				print e, url
				writer.writerow([url, "junk", "junk", "junk"])
				pass


	
if __name__ == "__main__":

	website = sys.argv[1]
	article_pkl = sys.argv[2]
	csv_file = sys.argv[3]

	# Load URL list from pickle file
	with open(article_pkl, 'rb') as pkl_file:
		article_urls = pickle.load(pkl_file)

	#Parse each article
	if website.lower() == "armenpress":
		parseArticlesArmenpress(article_urls, csv_file)
	elif website.lower() == "rferl":
		parseArticlesRFERL(article_urls, csv_file)


			







