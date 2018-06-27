# Classifier for Armenia Project
# Gautam Visveswaran, May 2018

import re, os, sys, pandas, pickle, csv
import numpy as np
from sklearn.svm import *
from sklearn.preprocessing import *
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.calibration import CalibratedClassifierCV
from utils import *
from englishpreprocessor import englishPreprocess

#Creates a matrix with each row representing a article and each column representing a unique word
def generateTrainFeatureMatrix(article_list, corpus_dict, category_dict):

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
def generateClassifiers(training_articles, corpus_dict, category_dict, C=.1):

	#Get feature and label matrices for training data
	features, relevant_labels, category_labels = generateTrainFeatureMatrix(training_articles, corpus_dict, category_dict)

	#Create SVM object
	svm_relevant = LinearSVC(C=C)
	svm_category = LinearSVC(C=C)

	clf_relevant = CalibratedClassifierCV(svm_relevant)
	clf_category = LinearSVC(C=C)
	# clf_category = CalibratedClassifierCV(svm_category)

	#Fit to training data
	clf_relevant.fit(features, relevant_labels)
	clf_category.fit(features, category_labels)

	return clf_relevant, clf_category



#Runs SVM classifier using 5-folding and returns how accurately the trained classifier predicts relevancy
def kFoldSVM(article_list, corpus_dict, category_dict, C):

	total_accuracy_relevant = 0.0
	total_accuracy_category = 0.0
	total_f1_relevant = 0.0
	total_f1_category = 0.0

	k_fold_range = 5

	for k in range(k_fold_range):

		#Obtain testing and training sets
		training_articles, testing_articles = getKFoldTrainTestSets(article_list, k, k_fold_range)
		
		#Train classifiers
		clf_relevant, clf_category = generateClassifiers(training_articles, corpus_dict, category_dict, C)

		#Get feature and correct label matrices for test data
		test_feature_matrix, correct_labels_relevant, correct_labels_category = generateTrainFeatureMatrix(testing_articles, corpus_dict, category_dict)

		total_accuracy_relevant += clf_relevant.score(test_feature_matrix, correct_labels_relevant)
		total_accuracy_category += clf_category.score(test_feature_matrix, correct_labels_category)

		try:
			total_f1_relevant += f1_score(clf_relevant.predict(test_feature_matrix), correct_labels_relevant)
			# total_f1_category += f1_score(clf_category.predict(test_feature_matrix), correct_labels_category)
		except:
			print "Invalid F1 Score: No true samples found"
	
	
	return total_accuracy_relevant/k_fold_range, total_accuracy_category/k_fold_range, total_f1_relevant/k_fold_range, total_f1_category/k_fold_range




#Splits input data into two sets, one to train with and one to test with
def getKFoldTrainTestSets(article_list, k, k_fold_range):

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

#Maintains dict of all unique categories possible
def store_categories(category_dict, csv_data):

	if "N/A" not in category_dict:
		category_dict["N/A"] = 0

	#Assign a unique integer to each category
	index = len(category_dict)+1

	for row in csv_data:

		if row['Category'] in ["N/A","", " ", "n/a", "n/A", "N/a"]:
			continue

		if row['Category'].strip() not in category_dict:

			category_dict[row['Category'].strip()] = index
			index += 1


	return category_dict

#Parses input files
def parseTrainingArticles(input_files, category_dict):

	train_article_list = []
	
	for csv_file in input_files:

		#Map each category to a unique integer (for classification)
		article_data = csv.DictReader(open(csv_file))
		store_categories(category_dict, article_data)

		#Store article data
		article_data = csv.DictReader(open(csv_file))

		#Store tokens, relevance, and category for each row
		for row in article_data:

			article = {}

			#Irrelevant rows
			if row["Category"] in ["N/A","", " ", "n/a", "n/A", "N/a"]:

				article['relevant'] = 'no'
				article['category'] = "N/A"

			#Relevant rows		
			elif row["Category"]:

				article['relevant'] = 'yes'
				article['category'] = str(row["Category"]).strip()

			else:
				continue

			article['tokens'] = englishPreprocess(row["Text"])
			train_article_list.append(article)

	return train_article_list, category_dict

#Function to try various C values, returns optimal C_val for raw accuracy
def determineBestCValue(train_article_list, corpus_dict, category_dict):

	C_vals = {.001:0, .01:0, .1:0, 1:0, 10:0, 100:0, 1000:0}
	best_C_val = .001

	for C in C_vals:	
		predicted_accuracy_relevant, predicted_accuracy_category = kFoldSVM(train_article_list, corpus_dict, category_dict, C)
		C_vals[C] = predicted_accuracy_relevant
	
	for C in C_vals:
		if C_vals[C] > C_vals[best_C_val]:
			best_C_val = C 

	return best_C_val

#Main
if __name__ == '__main__':

	#Parse articles from CSV
	num_input_files = int(sys.argv[1])
	input_files = []
	for i in range(num_input_files):
		input_files.append(sys.argv[i + 2])
	category_dict = {}
	train_article_list, category_dict = parseTrainingArticles(input_files, category_dict)
	
	
	#Load all unique words in corpus
	with open("corpus_dict.pkl", 'rb') as corpus_dict_file:
		corpus_dict = pickle.load(corpus_dict_file)
	
	
	#Calculate best C_value to be used in classifier 
	best_C_val  = 1
	# best_C_val = determineBestCValue(train_article_list, corpus_dict, category_dict)
	
	# Print predicted performance
	predicted_accuracy_relevant, predicted_accuracy_category, predicted_f1_relevant, predicted_f1_category = kFoldSVM(train_article_list, corpus_dict, category_dict, best_C_val)
	print "Predicted accuracy (relevant): ", predicted_accuracy_relevant
	print "Predicted F1 (relevant): ", predicted_f1_relevant


	# #Train and store classifiers
	clf_relevant, clf_category = generateClassifiers(train_article_list, corpus_dict, category_dict, best_C_val)
	with open("trained_classifiers.pkl", 'wb') as trained_classifier_file:
		pickle.dump(clf_relevant, trained_classifier_file, protocol=pickle.HIGHEST_PROTOCOL)
		pickle.dump(clf_category, trained_classifier_file, protocol=pickle.HIGHEST_PROTOCOL)



	
			







