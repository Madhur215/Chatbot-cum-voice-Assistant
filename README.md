# Chatbot
This a chatbot cum voice assistant that can be used for different purposes. It can do the following tasks:
1. Normal conversation through voice.
2. Get your all events or particular ones from your google calender.
3. Make a google search of your query and open up the browser with the results.
4. Make notes to write down something using notepad.

WORKING:
The working of the assistant is pretty simple.
First, a simple GUI shows up, in which you can see all your ongoing conversation.
When we click on the speak icon, it detects the voice and converts it to text using
speech_recognition module. 
On the text, first NLP is applied that creates a bag of words model which is then passed to a pretrained neural network made using the tflearn module. This network returns the "tag" with whichthe sentence is associated(see intents.json). 
This "tag" is then used to find the "sub tag" with which the sentence is associated
again with the help of the same model.
Once, the subtags is determined, it returns the appropriate answer associated with that
subtag, and the pyttsx3 module is used to speak the answer.
All the features like extracting the events from Google Calender have been defined
inside the calender.py file and the NLP has been applied in prepare.py
For the working with Google Calender you first need to get an API_KEY from Google developers page.


