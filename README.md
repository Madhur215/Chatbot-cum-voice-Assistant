# Chatbot
This a chatbot cum voice assistant that can be used for different purposes. It can do the following tasks:
1. Normal conversation through voice.
2. Get your all events or particular ones from your google calender.
3. Make a google search of your query and open up the browser with the results.
4. Make notes to write down something using notepad.

WORKING:
The model is made using tflearn module to make the neural network which takes the sentence from the user and gives an appropriate tag, with which it thinks the sentence is related to(refer to the intents.json file).
There are actually two models used in this, one to find the tag and other to find the sub-tag in the given tag. This increases the accuracy of the model and helps get better and likely results. 



