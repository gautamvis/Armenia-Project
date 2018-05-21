import re, os, sys, pandas, pickle
import numpy as np
from sklearn.svm import *
from sklearn.preprocessing import *
from sklearn.metrics import accuracy_score
from utils import *
from englishpreprocessor import englishPreprocess


#Creates a matrix with each row representing a article and each column representing a unique word
def generateFeatureMatrix(article_list, corpus_dict):

	#Determine dimensions of feature matrix, populate with 0s
	num_articles = len(article_list)
	num_features = len(corpus_dict)
	feature_matrix = np.zeros((num_articles, num_features))
	label_matrix = np.zeros(num_articles)

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

		# Add entry to label matrix
		if article['relevant_to_armenia_label'] == 'Yes':
			label_matrix[index] = 1
		elif article['relevant_to_armenia_label'] == 'No':
			label_matrix[index] = 2


	return feature_matrix, label_matrix


#Creates and fits a Linear SVM classifier, given a feature matrix, correct labels, and hyperparameter C as input
def generateClassifier(features, labels, C=.1):

	#Create SVM object
	clf = LinearSVC(C=C)

	#Fit to training data
	clf.fit(features, labels)

	return clf


#Runs SVM classifier using 5-folding and returns how accurately the trained classifier predicts relevancy
def runSVM(article_list, corpus_dict, C):


	#Total number of features
	num_features = len(corpus_dict)

	#Select a training and testing set
	total_test_features = []
	total_accuracy = 0.0

	for k in range(5):

		#Obtain testing and training sets
		training_articles, testing_articles = getTrainTestSets(article_list, k)
		
		#Get feature and label matrices for training data
		train_feature_matrix, train_label_matrix = generateFeatureMatrix(training_articles, corpus_dict)
		
		#Train classifier
		clf = generateClassifier(train_feature_matrix, train_label_matrix, C)

		#Get feature and correct label matrices for test data
		test_feature_matrix, correct_labels = generateFeatureMatrix(testing_articles, corpus_dict)

		#Predict
		num_correct_preds = 0.0
		predictions = clf.predict(test_feature_matrix)

		#Count number of correct predictions
		for index, prediction in enumerate(predictions):

			if prediction == correct_labels[index]:
				num_correct_preds += 1
			
	
		accuracy = num_correct_preds / len(correct_labels)
		

		total_accuracy += accuracy

	
	return total_accuracy/5

#Splits input data into two sets, one to train with and one to test with
def getTrainTestSets(article_list, k):

	#Define training and testing sets
	training_set = []
	testing_set = []
	
	#Iterate through all articles
	for index, article in enumerate(article_list):

		#Use five folding to split into training and testing sets
		if index % 5 == k:
			
			testing_set.append(article)
			
		else:
			
			training_set.append(article)
		

	return training_set, testing_set

#Main
if __name__ == '__main__':

	#Get articles from CSV
	article_file = sys.argv[1]
	csv_data = pandas.read_csv(article_file).values


	article_list = []

	for index, row in enumerate(csv_data):

		article = {}
		text = row[6]
		tokens = englishPreprocess(text)
		relevant_to_armenia_label = row[7]
		article['tokens'] = tokens
		article['relevant_to_armenia_label'] = relevant_to_armenia_label
		article_list.append(article)


	#Load all unique words in corpus
	with open("corpus_dict.pkl", 'rb') as corpus_dict_file:
		corpus_dict = pickle.load(corpus_dict_file)

	
	#TODO: optimal C value
	c = 0.1


	#Run SVM to predict relevance
	accuracy = runSVM(article_list, corpus_dict, c)
	
	print accuracy

	