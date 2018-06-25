import sys, pandas, pickle, csv, re
from english_preprocessor import englishPreprocess

#Create corpus dictionary
def createCorpusDict(all_words):

	corpus_dict = {}
	word_count = 0

	for word in all_words:
		if word not in corpus_dict:
			corpus_dict[word] = word_count
			word_count += 1

	return corpus_dict

def is_ascii(input):
    try:
        input.decode('ascii')
        return True
    except:
    	if input.find("'") == -1:
        	return False
        return True


def createDict():
	
	#Read in CSV file with articles
	num_input_files = int(sys.argv[1])
	input_files = []
	for i in range(num_input_files):
		input_files.append(sys.argv[i + 2])

	text = ""
	for file in input_files:

		article_data = csv.DictReader(open(file))

		for row in article_data:
			if row['Text']:
				text += " " + row['Text']	


	#Preprocess
	all_words = englishPreprocess(text)

	corpus_dict = createCorpusDict(all_words)

	return corpus_dict

if __name__ == '__main__':
	
	corpus_dict = createDict()

	#Write dict to pkl file
	with open("corpus_dict.pkl", 'wb') as corpus_dict_file:
		pickle.dump(corpus_dict, corpus_dict_file, protocol=pickle.HIGHEST_PROTOCOL)









