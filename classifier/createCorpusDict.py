import sys, pandas, pickle
from englishpreprocessor import englishPreprocess

#Create corpus dictionary
def createCorpusDict(all_words):

	corpus_dict = {}
	word_count = 0

	for word in all_words:
		if word not in corpus_dict:
			corpus_dict[word] = word_count
			word_count += 1

	return corpus_dict



if __name__ == '__main__':

	#Read in CSV file with articles
	article_file = sys.argv[1]	
	df = pandas.read_csv(article_file).values

	#Get a concatenated object with all words
	text = ""
	for row in df:
		text += row[8]

	#Preprocess
	all_words = englishPreprocess(text)

	corpus_dict = createCorpusDict(all_words)

	print corpus_dict

	with open("corpus_dict.pkl", 'wb') as corpus_dict_file:
		pickle.dump(corpus_dict, corpus_dict_file, protocol=pickle.HIGHEST_PROTOCOL)