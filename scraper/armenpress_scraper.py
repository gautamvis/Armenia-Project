# Scraper for Armenia Project
# Gautam Visveswaran, May 2018

import errno, json, os, pickle, re, shutil, string, sys, unicodedata, time, math
import unicodecsv as csv
from requests import get
from bs4 import *
from threading import Thread
from selenium import webdriver


#Gets list of articles to parse from armenpress
def runDriverArmenpress(category=None, num_articles=40):

	# print "Starting to scrape armenpress.am "
	# if category is not None:
	#   print "Finding articles relating to ", category 
	
	article_urls = []
	base_url = "https://armenpress.am"

	#Initialize driver
	driver = webdriver.Chrome("/Users/gautam/Desktop/armeniaProject/scraper/chromedriver")

	driver.get("https://armenpress.am/eng/news/society/")

	# Loop for more articles
	load_more_button = driver.find_element_by_id('morenewsbydatecontainer')
	# for i in range(num_articles/40 - 1): 
	# 	load_more_button.click()

	article_elements = driver.find_elements_by_class_name('newsbycatitem')

	for article in article_elements:
		article_urls.append(article.find_element_by_tag_name("a").get_attribute('href'))

	#Quit webdriver 
	driver.quit()
	
	return article_urls

	
if __name__ == "__main__":

	
	#Get articles to be scraped
	article_urls = runDriverArmenpress()

	#Save url list to pickle file
	with open("article_urls.pkl", 'wb') as pkl_file:
		pickle.dump(article_urls, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)


	#TODO thread to improve speed	

	#TODO: Print metrics for dataset

   
