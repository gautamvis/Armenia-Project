import sys, pandas, pickle, csv, re
from englishpreprocessor import englishPreprocess, remove_punctuation

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



if __name__ == '__main__':

	#Read in CSV file with articles
	num_input_files = int(sys.argv[1])
	input_files = []
	for i in range(num_input_files):
		input_files.append(sys.argv[i + 2])

	text = ""
	for file in input_files:

		article_data = csv.DictReader(open(file))

		for row in article_data:
			#Only add relevant marked rows from rferl set
			if row['Category']:
				text += row['Text']	

	#Remove escape characters
	cleanText = ""
	for word in text.split():
		try:
			re.sub(re.compile('<.*?>'), '', word.encode('utf-8'))
			word = remove_punctuation(word)
			cleanText += word + " "
		except:
			pass

	#Preprocess
	all_words = englishPreprocess(cleanText)

	corpus_dict = createCorpusDict(all_words)


	#FIXME remove after testing
	# print corpus_dict
	# exit(0)

	#Write dict to pkl file
	with open("corpus_dict.pkl", 'wb') as corpus_dict_file:
		pickle.dump(corpus_dict, corpus_dict_file, protocol=pickle.HIGHEST_PROTOCOL)









