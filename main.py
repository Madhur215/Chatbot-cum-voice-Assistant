import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import json
import random
from model import create_model
import tensorflow as tf

with open("intents.json") as file:
	data = json.load(file)

# try:



# except:
	tags = []				 # Contains all the different tags	
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

	all_questions_train = np.array(all_questions_train)
	tags_output = np.array(tags_output)

	tf.reset_default_graph()
	model = create_model(all_questions_train, tags_output, tags, all_question_words)
	model.fit_model(all_questions_train, tags_output)

	# Preparing sub tags models
	sub_tags_list = []
	sub_tags_models = []

	for intent in data["intents"]:

		all_words_sub_questions = []
		all_sub_tags = []
		sub_question_tags = []
		all_sub_questions_list = []

		for sub_tags in intent["sub_tags"]:
			for questions in sub_tags["questions"]:
				tk_words = nltk.word_tokenize(questions)
				all_words_sub_questions.extend(tk_words)
				all_sub_questions_list.append(tk_words)
				sub_question_tags.append(sub_tags["sub"])

			if sub_tags["sub"] not in all_sub_tags:
				all_sub_tags.append(sub_tags["sub"])

		all_words_sub_questions = [stemmer.stem(w.lower()) for w in all_words_sub_questions if w != "?" and "!"]
		all_words_sub_questions = sorted(list(set(all_words_sub_questions)))
		all_sub_tags = sorted(all_sub_tags)

		all_sub_questions_train = []
		sub_tags_output = []
		r = [0 for _ in range(len(all_sub_tags))]
	
		for i, word in enumerate(all_sub_questions_list):
			bag_of_words = []
			word = [stemmer.stem(w.lower()) for w in word]
			for wr in all_words_sub_questions:

				if wr in word:
					bag_of_words.append(1)
				else:
					bag_of_words.append(0)

			row = r[:]
			row[all_sub_tags.index(sub_question_tags[i])] = 1
			all_sub_questions_train.append(bag_of_words)
			sub_tags_output.append(row)

		all_sub_questions_train = np.array(all_sub_questions_train)
		sub_tags_output = np.array(sub_tags_output)

		sub_model = create_model(all_sub_questions_train, sub_tags_output, all_sub_tags, all_words_sub_questions)
		sub_model.fit_model(all_sub_questions_train, sub_tags_output)
		sub_tags_models.append(sub_model)
		
		sub_tags_list.extend(all_sub_tags)

	def start_chat():

		print("Welcome!")
		while True:

			sentence = input("You: ")
			if sentence.lower() == "exit":
				break

			tag = model.predict_tag(sentence)
			sub_tag = sub_tags_models[tag].predict_tag(sentence)
			print(sub_tags_list[sub_tag])

			# TODO only sub tags index being returned. Need to compare the tag also 
			# to print the result!!

	start_chat()













