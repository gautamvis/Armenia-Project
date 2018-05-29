import re, os, sys, pandas, pickle, csv
import numpy as np
from sklearn.svm import *
from sklearn.preprocessing import *
from sklearn.metrics import accuracy_score
from utils import *
from englishpreprocessor import englishPreprocess


#Creates a matrix with each row representing a article and each column representing a unique word
def generateFeatureMatrix(article_list, corpus_dict, keyword_dict):

	#Determine dimensions of feature matrix, populate with 0s
	num_articles = len(article_list)
	num_features = len(corpus_dict)
	feature_matrix = np.zeros((num_articles, num_features))
	relevant_label_matrix = np.zeros(num_articles)
	keyword_label_matrix = np.zeros(num_articles)

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

		# Add entry to label matrices
		if article['relevant'].lower() == 'yes':
			relevant_label_matrix[index] = 1
			keyword_label_matrix[index] = keyword_dict[article['keyword']]
		
		elif article['relevant'].lower() == 'no':
			relevant_label_matrix[index] = 2
			keyword_label_matrix[index] = keyword_dict['junk']

		else:
			print "Error with labels, index ", index, " label ", article['relevant'].lower()
			exit(0)


	return feature_matrix, relevant_label_matrix, keyword_label_matrix


#Creates and fits a Linear SVM classifier, given a feature matrix, correct labels, and hyperparameter C as input
def generateClassifier(features, labels, C=.1):

	#Create SVM object
	clf = LinearSVC(C=C)

	#Fit to training data
	clf.fit(features, labels)

	return clf


#Runs SVM classifier using 5-folding and returns how accurately the trained classifier predicts relevancy
def runSVM(article_list, corpus_dict, keyword_dict, C):


	#Total number of features
	num_features = len(corpus_dict)

	#Select a training and testing set
	total_test_features = []
	total_accuracy_relevant = 0.0
	total_accuracy_keyword = 0.0

	#TODO: optimal k-folding range
	k_fold_range = 5

	for k in range(k_fold_range):

		#Obtain testing and training sets
		training_articles, testing_articles = getTrainTestSets(article_list, k, k_fold_range)
		
		#Get feature and label matrices for training data
		train_feature_matrix, train_label_matrix_relevant, train_label_matrix_keyword = generateFeatureMatrix(training_articles, corpus_dict, keyword_dict)
		
		#Train classifiers
		clf_relevant = generateClassifier(train_feature_matrix, train_label_matrix_relevant, C)
		clf_keyword = generateClassifier(train_feature_matrix, train_label_matrix_keyword, C)

		#Get feature and correct label matrices for test data
		test_feature_matrix, correct_labels_relevant, correct_labels_keyword = generateFeatureMatrix(testing_articles, corpus_dict, keyword_dict)

		#Predict
		num_correct_preds_relevant = 0.0
		num_correct_preds_keyword = 0.0
		predictions_relevant = clf_relevant.predict(test_feature_matrix)
		predictions_keyword = clf_keyword.predict(test_feature_matrix)

		#Count number of correct predictions
		for index, prediction in enumerate(predictions_relevant):

			if prediction == correct_labels_relevant[index]:
				num_correct_preds_relevant += 1
		
		for index, prediction in enumerate(predictions_keyword):

			if prediction == correct_labels_keyword[index]:
				num_correct_preds_keyword += 1
	
		accuracy_relevant = num_correct_preds_relevant / len(correct_labels_relevant)
		accuracy_keyword = num_correct_preds_keyword / len(correct_labels_keyword)

		total_accuracy_relevant += accuracy_relevant
		total_accuracy_keyword += accuracy_keyword

	
	return total_accuracy_relevant/k_fold_range, total_accuracy_keyword/k_fold_range

#Splits input data into two sets, one to train with and one to test with
def getTrainTestSets(article_list, k, k_fold_range):

	#Define training and testing sets
	training_set = []
	testing_set = []
	
	#Iterate through all articles
	for index, article in enumerate(article_list):

		#Use five folding to split into training and testing sets
		if index % k_fold_range == k:
			
			testing_set.append(article)
			
		else:
			
			training_set.append(article)
		

	return training_set, testing_set

def storeKeywords(csv_data):

	keyword_dict = {}

	#Label junk articles as 0
	keyword_dict['junk'] = 0

	#Assign a unique integer to each keyword
	index = 1

	for row in csv_data:

		if row[0] not in keyword_dict:

			keyword_dict[row[0]] = index
			index += 1


	return keyword_dict


#Main
if __name__ == '__main__':

	#Get articles from CSV
	article_file = sys.argv[1]
	csv_data = pandas.read_csv(article_file).values
	
	
	#Map each keyword to a unique integer (for classification)
	keyword_dict = storeKeywords(csv_data)

	article_list = []

	#Store tokens, relevance, and keyword for each row
	for index, row in enumerate(csv_data):
		
		#Incomplete information in row
		if pandas.isnull(row[0]) or pandas.isnull(row[8]) or pandas.isnull(row[9]):
			# print "Incomplete row: ", index
			continue
		if row[0] is None or row[8] is None or row[9] is None:
			continue

		article = {}
		article['tokens'] = englishPreprocess(row[8])
		article['relevant'] = str(row[9])
		article['keyword'] = str(row[0])
		article_list.append(article)

	#Load all unique words in corpus
	with open("corpus_dict.pkl", 'rb') as corpus_dict_file:
		corpus_dict = pickle.load(corpus_dict_file)
	
	#TODO: optimal C value
	c = 0.1

	#Run SVM to predict relevance
	accuracy_relevant, accuracy_keyword = runSVM(article_list, corpus_dict, keyword_dict, c)
	
	print "Number of unique keywords: ", len(keyword_dict)
	print "Accuracy (relevance): ", accuracy_relevant
	print "Accuracy (keyword): ", accuracy_keyword

