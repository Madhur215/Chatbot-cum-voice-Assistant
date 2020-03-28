import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np


class prepare_data:

	def __init__(self, data):
		self.all_words = []
		self.all_tags = []
		self.all_words_lists = []
		self.tags_lists = []
		self.data = data

	def prepare(self, level1_data, level1_index, level2_index, tag):

		for content in level1_data[level1_index]:
			for dt in content[level2_index]:
				token_words = nltk.word_tokenize(dt)
				self.all_words.extend(token_words)
				self.all_words_lists.append(token_words)
				self.tags_lists.append(content[tag])

			if content[tag] not in self.all_tags:
				self.all_tags.append(content[tag])



		stemmer = LancasterStemmer()		
		self.all_words = [stemmer.stem(w.lower()) for w in self.all_words if w != "?" and "!"]
		self.all_words = sorted(list(set(self.all_words)))

		return self.all_words, self.all_tags, self.all_words_lists, self.tags_lists

	def get_training_set(self):

		self.questions_train = []
		self.tags_output = []
		r = [0 for _ in range(len(self.all_tags))]
		for i, word in enumerate(self.all_words_lists):
			bag_of_words = []
			stemmer = LancasterStemmer()
			word = [stemmer.stem(w.lower()) for w in word]
			for wr in self.all_words:

				if wr in word:
					bag_of_words.append(1)
				else:
					bag_of_words.append(0)

			row = r[:]
			row[self.all_tags.index(self.tags_lists[i])] = 1
			self.questions_train.append(bag_of_words)
			self.tags_output.append(row)

		return self.questions_train, self.tags_output




