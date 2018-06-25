# Armenia Project

## TODO 

-Fix Armenpress Scraper
-Print predicted probabilities
-Update Readme


Tools:
Python 2.7.15
Python libraries required: sklearn, pandas, numpy, bs4, requests, selenium
Chromedriver (can be downloaded from http://chromedriver.chromium.org/)


### Contents: 

Note: All functions are run on command line, arguments needed are specified

#### Scraper

Contains implementation of RFERL and Armenpress scrapers

Files:
Chromedriver (must be inside this directory to run)

armenpress_scraper.py
	Arguments(1): number of articles to be scraped 
	Ex. $ python armenpress_scraper.py 50
	Saves links to armenpress_article_urls.pkl


rferl_scraper.py 
	Arguments(2): page to start scraping and page to end scraping. Must be in range (0-274)
	Ex. $ python rferl_scraper.py 0 15
	Saves links to rferl_article_urls.pkl


parser.py
	Arguments(3): website name ("rferl" or "armenpress"), path to pkl file with URLs, csv file to output 
	Ex. $ python parser.py rferl /path/to/rferl_article_urls.pkl /path/to/rferl_output.csv
	Saves trained classifier and dictionary of categories to trained_classifiers.pkl


#### Classifier

Contains code to train and run classifier
**Note: Train csv files must include headings "Category" and "Text". A blank is equivalent to "N/A" in the Category column. 
CSV files to be classified must include heading "Text".
CSV files must be well formed and cannot include blank rows**

Files:

train_classifier.py
	Arguments(2+): number of input training csv files, list of training csv files
	Ex. $ python train_classifer.py 2 /path/to/train_file_1.csv /path/to/train_file_2.csv

run_classifier.py
	Arguments(2+): number of input csv files, list of training csv files




#### Datasets








