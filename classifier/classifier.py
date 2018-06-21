import re, os, sys, pandas, pickle, csv
import numpy as np
from sklearn.svm import *
from sklearn.preprocessing import *
from sklearn.metrics import accuracy_score
from utils import *
from englishpreprocessor import englishPreprocess

#Creates a matrix with each row representing a article and each column representing a unique word
def generateFeatureMatrix(article_list, corpus_dict, category_dict):

	#Determine dimensions of feature matrix, populate with 0s
	num_articles = len(article_list)
	num_features = len(corpus_dict)
	feature_matrix = np.zeros((num_articles, num_features))
	relevant_label_matrix = np.zeros(num_articles)
	category_label_matrix = np.zeros(num_articles)

	#Create a row in the feature matrix for each article
	for index,article in enumerate(article_list):

		article_matrix = np.zeros(num_features)

		#Increment counts of words observed in an article
		for word in article['tokens']: 				       
			if word in corpus_dict:
				article_matrix[corpus_dict[word]] += 1

			else:
				print word
		
		# Normalize
		article_matrix = article_matrix / np.linalg.norm(article_matrix)

		# Add row to feature matrix
		feature_matrix[index] = article_matrix

		# Add entry to label matrices
		if article['relevant'].lower() == 'yes':
			relevant_label_matrix[index] = 1
			category_label_matrix[index] = category_dict[article['category']]
		
		elif article['relevant'].lower() == 'no':
			relevant_label_matrix[index] = 2
			category_label_matrix[index] = category_dict['N/A']

		else:
			print "Error with labels, index ", index, " label ", article['relevant'].lower()
			exit(0)


	return feature_matrix, relevant_label_matrix, category_label_matrix


#Creates and fits a Linear SVM classifier, given a feature matrix, correct labels, and hyperparameter C as input
def generateClassifier(features, labels, C=.1):

	#Create SVM object
	clf = LinearSVC(C=C)
	# clf = SVC(kernel='linear', probability=True)

	#Fit to training data
	clf.fit(features, labels)

	return clf



#Runs SVM classifier using 5-folding and returns how accurately the trained classifier predicts relevancy
def runSVM(article_list, corpus_dict, category_dict, C):

	total_accuracy_relevant = 0.0
	total_accuracy_category = 0.0

	k_fold_range = 5

	for k in range(k_fold_range):

		#Obtain testing and training sets
		training_articles, testing_articles = getTrainTestSets(article_list, k, k_fold_range)
		
		#Get feature and label matrices for training data
		train_feature_matrix, train_label_matrix_relevant, train_label_matrix_category = generateFeatureMatrix(training_articles, corpus_dict, category_dict)
		
		#Train classifiers
		clf_relevant = generateClassifier(train_feature_matrix, train_label_matrix_relevant, C)
		clf_category = generateClassifier(train_feature_matrix, train_label_matrix_category, C)

		#Get feature and correct label matrices for test data
		test_feature_matrix, correct_labels_relevant, correct_labels_category = generateFeatureMatrix(testing_articles, corpus_dict, category_dict)

		#Predict
		# prediction_probabilities = clf_relevant.predict_proba(test_feature_matrix)
		# print prediction_probabilities
		# exit(0)
	
		total_accuracy_relevant += clf_relevant.score(test_feature_matrix, correct_labels_relevant)
		total_accuracy_category += clf_category.score(test_feature_matrix, correct_labels_category)

	
	return total_accuracy_relevant/k_fold_range, total_accuracy_category/k_fold_range

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

def store_categories(category_dict, csv_data):

	if "N/A" not in category_dict:
		category_dict["N/A"] = 0

	#Assign a unique integer to each category
	index = len(category_dict)+1

	for row in csv_data:

		if row['Category'] not in category_dict:

			category_dict[row['Category']] = index
			index += 1


	return category_dict


#Main
if __name__ == '__main__':

	#Get articles from CSV
	num_input_files = int(sys.argv[1])
	input_files = []
	for i in range(num_input_files):
		input_files.append(sys.argv[i + 2])
	

	article_list = []
	category_dict = {}

	for csv_file in input_files:

		#Map each category to a unique integer (for classification)
		article_data = csv.DictReader(open(csv_file))
		store_categories(category_dict, article_data)

		#Store article data
		article_data = csv.DictReader(open(csv_file))

		#Store tokens, relevance, and category for each row
		for row in article_data:

			article = {}

			#Relevant rows		
			if row["Category"] and row["Category"] != "N/A":

				article['relevant'] = 'yes'
				article['category'] = str(row["Category"])
				

			#Irrelevant rows
			elif row["Category"] in ["N/A",""]:

				article['relevant'] = 'no'
				article['category'] = "N/A"

			else:
				continue

			# print row["Category"]
			article['tokens'] = englishPreprocess(row["Text"])
			article_list.append(article)

	
	#Load all unique words in corpus
	with open("corpus_dict.pkl", 'rb') as corpus_dict_file:
		corpus_dict = pickle.load(corpus_dict_file)
	
	#TODO: optimal C value
	c = 10

	
	#Run SVM to predict relevance
	accuracy_relevant, accuracy_category = runSVM(article_list, corpus_dict, category_dict, c)
	
	print "Number of unique categorys: ", len(category_dict)
	print "Accuracy (relevance): ", accuracy_relevant
	# print "Accuracy (category): ", accuracy_category
