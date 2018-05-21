from requests import get
from bs4 import *
import errno, json, os, pickle, re, shutil, string, sys, unicodedata
from threading import Thread
from selenium import webdriver
import time



#Gets list of articles to parse from armenpress
def runDriverArmenpress(category=None):

	# print "Starting to scrape armenpress.am "
	# if category is not None:
	# 	print "Finding articles relating to ", category 
	
	article_urls = []
	base_url = "https://armenpress.am"

	#Initialize driver
	driver = webdriver.Chrome("/Users/gautam/Desktop/armeniaProject/scraper/chromedriver")

	driver.get("https://armenpress.am/eng/news/society/")

	# load_more_button = driver.find_element_by_id('morenewsbydatecontainer')
	# load_more_button.click()

	article_elements = driver.find_elements_by_class_name('newsbycatitem')

	print len(article_elements)
	for article in article_elements:
		print article.find_element_by_id

	#TODO
		#Add articles to list

		#class = newsbycatitem, get the href

		#Break if cant load anymore



	driver.quit()
	

	return article_urls


# Strips whitespace
def sanitizeText(text):
	text = str(text)
	text = text.replace('\r', '')
	text = text.replace('\n', '')
	text = re.sub(' +',' ',text)
	text = text.lstrip()
	text = text.rstrip()
	return text


# Thread function takes in URL and collects articles
def runScraperArmenpress(article_urls):


	

	for article_url in article_urls:

		try:

			#Get the article 
			univ_response = get(page)
	
			#Parse with beautifulsoup
			univ_html_soup = BeautifulSoup(univ_response.text, "html.parser")

			#Find class opennewstitle and class articleBody


			#TODO: other parsers?

			#Add relevant info to csv

		except:
			pass

	print "Finished scraping"


# Cleans up directory
def cleanDirectory(location, directory):
	
	if os.path.exists(location):
		# Remove relevant directories
		if directory:
			shutil.rmtree(location)
	
		# Remove relevant files
		else:	
			os.remove(location)
	
if __name__ == "__main__":

	
	# cleanDirectory()

	# Create directories for individual reviews and concatenated reviews
	# if not os.path.exists("scraped_articles"):
	# 	os.makedirs("scraped_articles")

	# Enter individual_reviews during scraping
	# os.chdir(os.getcwd()+"scraped_articles")

	# thread_pool = []

	# urls = []

	runDriverArmenpress()

	#TODO: populate URLs	
	

	#Create a thread to crawl each college, store in thread_pool list
	# for url in urls:
	# 	try:
	# 		thread = Thread(target = runScraperArmenpress, args = (url,))
	# 		thread_pool.append(thread)
	# 	except: 
	# 		pass

	# Start all threads
	# for thread in thread_pool:
	# 	thread.start()

	# Join all threads
	# for thread in thread_pool:
	# 	thread.join()
	

	#TODO: Print metrics for dataset

   
