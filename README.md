# Armenia Project



## Requirements:

[Python 2.7.15](https://www.python.org/downloads/)

Python libraries: sklearn, pandas, numpy, bs4, requests, selenium

[Chromedriver](http://chromedriver.chromium.org/)


## Contents: 

**Note: All functions are run on command line, arguments needed are specified**


### Scraper

Contains implementation of RFERL and Armenpress scrapers

#### Files:

Chromedriver (must be inside this directory to run)

*armenpress_scraper.py*
	
Arguments(1): number of articles to be scraped, in multiples of 40
	
	Ex. $ python armenpress_scraper.py 40
	
Saves links to armenpress_article_urls.pkl


*rferl_scraper.py*
	
Arguments(2): page to start scraping and page to end scraping. Must be in range (0-274)
	
	Ex. $ python rferl_scraper.py 0 15
	
Saves links to rferl_article_urls.pkl


*parser.py*

Arguments(3): website name ("rferl" or "armenpress"), path to pkl file with URLs, csv file to output 

	Ex. $ python parser.py rferl /path/to/rferl_article_urls.pkl /path/to/rferl_output.csv

Saves trained classifier and dictionary of categories to trained_classifiers.pkl


### Classifier

Contains code to create a dictionary of unique words and to train and run classifier

Training CSV files must include headings "Category" and "Text". A blank is equivalent to "N/A" in the Category column. 

CSV files to be classified must include headings "URL" and "Text".

Must be run in order: create_corpus_dict.py,  train_classifier.py, run_classifier.py**


**Note: Ensure all CSV files are well formed, have no special/hidden characters in first row, and don't include blank rows**


#### Files:

*create_corpus_dict.py*
	
Arguments(2+): number of input training csv files, list of training csv files

Outputs corpus_dict.pkl which contains a dictionary of all the words in the corpus	

*train_classifier.py*

Arguments(2+): number of input training csv files, list of training csv files

	Ex. $ python train_classifer.py 2 /path/to/train_file_1.csv /path/to/train_file_2.csv

Outputs trained_classifiers.pkl

*run_classifier.py*

Arguments(2+): number of input csv files, list of training csv files
	
		Ex. $ python run_classifier.py 2 /path/to/input_file_1.csv

Outputs predictions, with likelihood that the article is relevant

*english_preprocessor.py*

Contains functions to preprocess text from news articles before running classifier

*porterstemmer.py*

Contains stemmer function used for preprocessing

*englishstopwords.txt*

Contains stopwords used for preprocessing


### Datasets

Contains training datasets






