# Classifier for Armenia Project
# Gautam Visveswaran, May 2018

import re, os, sys, pandas, pickle, csv
import numpy as np
from sklearn.svm import *
from sklearn.preprocessing import *
from sklearn.metrics import recall_score, precision_score, f1_score
from utils import *
from englishpreprocessor import englishPreprocess
import getopt


#Parses input files
def parseArticles(input_files):

	article_list = []
	
	for csv_file in input_files:

		#Map each category to a unique integer (for classification)
		article_data = csv.DictReader(open(csv_file))

		#Store tokens, relevance, and category for each row
		for row in article_data:

			article = {}
			article['tokens'] = englishPreprocess(row["Text"])
			article['URL'] = row["URL"]
			article_list.append(article)

	return article_list

#Creates a matrix with each row representing a article and each column representing a unique word
def generateFeatureMatrix(article_list, corpus_dict):

	#Determine dimensions of feature matrix, populate with 0s
	num_articles = len(article_list)
	num_features = len(corpus_dict)
	feature_matrix = np.zeros((num_articles, num_features))

	#Create a row in the feature matrix for each article
	for index,article in enumerate(article_list):

		article_matrix = np.zeros(num_features)

		#Increment counts of words observed in an article
		for word in article['tokens']: 				       
			if word in corpus_dict:
				article_matrix[corpus_dict[word]] += 1

		# Normalize
		article_matrix = article_matrix / np.linalg.norm(article_matrix)

		# Add row to feature matrix
		feature_matrix[index] = article_matrix

	return feature_matrix


def runSVM(articles, corpus_dict):
	
	feature_matrix = generateFeatureMatrix(articles, corpus_dict)

	prediction_probabilities = clf_relevant.predict_proba(feature_matrix)
	for i, prediction in enumerate(prediction_probabilities):
		print articles[i]["URL"] + " " + "Likelihood of relevance: " + str(round(prediction[0],3)*100) + "%"



if __name__ == '__main__':

	#Parse articles from CSV
	num_input_files = int(sys.argv[1])
	input_files = []
	for i in range(num_input_files):
		input_files.append(sys.argv[i + 2])
	articles = parseArticles(input_files)

	# Load saved classifiers and dicts
	with open("trained_classifiers.pkl", 'rb') as trained_clf_file:
		clf_relevant = pickle.load(trained_clf_file)
		clf_category = pickle.load(trained_clf_file)
	with open("corpus_dict.pkl", 'rb') as corpus_dict_file:
		corpus_dict = pickle.load(corpus_dict_file)
	

	runSVM(articles, corpus_dict)




