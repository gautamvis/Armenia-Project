# Scraper for Armenia Project
# Gautam Visveswaran, May 2018

import errno, json, os, pickle, re, shutil, string, sys, unicodedata, time, math
import unicodecsv as csv
from requests import get
from bs4 import *
from threading import Thread
from selenium import webdriver


#Get all articles on Armenia between 2004 and 2008 from RFERL
def scrapeRFERL(startpage, endpage):

	start_url = "https://www.rferl.org/z/655?p="

	driver = webdriver.Chrome("/Users/gautam/Desktop/armeniaProject/scraper/chromedriver")

	all_links = []

	for i in range(startpage, endpage):

		driver.get(start_url + str(i))
		
		links = driver.find_elements_by_css_selector(".media-block.horizontal.with-date")

		for link in links:
			all_links.append(link.find_element_by_tag_name("a").get_attribute('href'))


	return all_links
	
if __name__ == "__main__":

	startpage = int(sys.argv[1])
	endpage = int(sys.argv[2])

	all_links = scrapeRFERL(startpage, endpage)

	with open("rferl_article_urls.pkl", 'wb') as pkl_file:
		pickle.dump(all_links, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)

   
