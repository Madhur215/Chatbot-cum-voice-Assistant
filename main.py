import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import json
import random
from model import create_model
import random
import tensorflow as tf
from prepare import prepare_data
import calender as cl
import pyttsx3
import speech_recognition as sr

stemmer = LancasterStemmer()
with open("intents.json") as file:
	data = json.load(file)


def speak(text):
	speaker = pyttsx3.init()
	speaker.say(text)
	speaker.runAndWait()

def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e:
			print("Exception: " + str(e))

	return said

tags = []				 # Contains all the different tags	
all_questions_list = []  # Contains the different question with their words tokenized
questions_tags = []		 # Contains the questions tags corresponding to the questions in above list
all_question_words = []	 # Contains all the words in all the questions of the dataset

pr = prepare_data(data)
all_question_words, tags, all_questions_list, questions_tags = pr.prepare(data, "intents", "all_questions", "tag")

all_questions_train = []
tags_output = []

all_questions_train, tags_output = pr.get_training_set()
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

	tr = prepare_data(data)
	all_words_sub_questions, all_sub_tags, all_sub_questions_list, sub_question_tags = tr.prepare(intent, "sub_tags", "questions", "sub")
		
	all_sub_questions_train = []
	sub_tags_output = []
	all_sub_questions_train, sub_tags_output = tr.get_training_set()
	all_sub_questions_train = np.array(all_sub_questions_train)
	sub_tags_output = np.array(sub_tags_output)

	sub_model = create_model(all_sub_questions_train, sub_tags_output, all_sub_tags, all_words_sub_questions)
	sub_model.fit_model(all_sub_questions_train, sub_tags_output)
	sub_tags_models.append(sub_model)
		
	sub_tags_list.extend(all_sub_tags)

tags_dict = {}
answers_dict = {}

def prepare_tags_list():
		
	for intent in data["intents"]:
		curr_tag = intent["tag"]
		s_tags_list = []
		for sub_tg in intent["sub_tags"]:
			curr_sub_tag = sub_tg["sub"]
			s_tags_list.append(curr_sub_tag)
			answers_dict[curr_sub_tag] = sub_tg["answers"]

		tags_dict[curr_tag] = s_tags_list

prepare_tags_list()

def start_chat():

	print("Welcome!")
	while True:

		print("Say something: ")
		sentence = get_audio()
		if sentence.lower() == "exit":
			break

		tag = model.predict_tag(sentence)
		sub = sub_tags_models[tag].predict_tag(sentence)
		tag_word = tags[tag]
			
		sub_list = tags_dict.get(tag_word)
		sub_tag_word = sub_list[sub]

		if sub_tag_word == "know-date":
			date = cl.get_date_for_day(sentence)
			speak(date)
			print("Boss: ", date)

		elif sub_tag_word == "get-events":
			day = cl.get_date(sentence)
			cl.get_selected_events(cl.authenticate(), day)
		else:
			ans = answers_dict.get(sub_tag_word)
			a = random.choice(ans)
			speak(a)
			print("Boss: ", a)

start_chat()	

# day date error










