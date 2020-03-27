import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import json
import random
from model import create_model

with open("intents.json") as file:
	data = json.load(file)

# try:



# except:
	tags = []				 # Contains all the different tags
	sub_tags = []	
	all_questions_list = []  # Contains the different question with their words tokenized
	questions_tags = []		 # Contains the questions tags corresponding to the questions in above list
	all_question_words = []	 # Contains all the words in all the questions of the dataset

	for intent in data["intents"]:
		for questions in intent["all_questions"]:

			token_words = nltk.word_tokenize(questions)
			all_question_words.extend(token_words)
			all_questions_list.append(token_words)
			questions_tags.append(intent["tag"])

		if intent["tag"] not in tags:
			tags.append(intent["tag"])


	stemmer = LancasterStemmer()
	all_question_words = [stemmer.stem(w.lower()) for w in all_question_words if w != "?" and "!"]
	all_question_words = sorted(list(set(all_question_words)))
	tags = sorted(tags)

	all_questions_train = []
	tags_output = []
	r = [0 for _ in range(len(tags))]

	for i, word in enumerate(all_questions_list):

		bag_of_words = []
		word = [stemmer.stem(w.lower()) for w in word]
		for wr in all_question_words:

			if wr in word:
				bag_of_words.append(1)
			else:
				bag_of_words.append(0)

		row = r[:]
		row[tags.index(questions_tags[i])] = 1
		all_questions_train.append(bag_of_words)
		tags_output.append(row)

	
	print(tags_output[2])
	all_questions_train = np.array(all_questions_train)
	tags_output = np.array(tags_output)

	# models = []

	model = create_model(all_questions_train, tags_output, tags, all_question_words)
	model.fit_model(all_questions_train, tags_output)

	def start_chat():

		print("Welcome!")
		while True:

			sentence = input("You: ")
			if sentence.lower() == "exit":
				break

			tag = model.predict_tag(sentence)
			print(tag)


	start_chat()













