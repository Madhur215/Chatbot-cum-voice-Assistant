# Chatbot cum Voice Assistant
This a chatbot cum voice assistant that can be used for different purposes. It can do the following tasks:
1. Normal conversation through voice.
2. Get your all events or particular ones from your google calender.
3. Make a google search of your query and open up the browser with the results.
4. Make notes to write down something using notepad.
5. Send emails using Gmail.
6. Open music and vs code application.
7. Search directly anything on Wikipedia.
8. Get real time weather report of your city.

## Screenshots of the project
![Image](/images/chatbot.jpg)

## Installation
* All the modules which are required for this application are stated in requirements.txt file. 
To install all of them rum the following command:
```
pip3 install -r requirements.txt
```

* Enable Google Calender API with your account here: https://developers.google.com/calendar/quickstart/python
* Get a weather api key by creating your account on https://openweathermap.org/api
* Create a keys.py file and add the following:
    * EMAIL = "your email id to send emails from"
    * PASSWORD = "pasword of your email id"
    * DICT = "A dictionary to store the emails of recipients"
    * WEATHER_KEY = "your weather api key"

## Working of the project
The working of the assistant is pretty simple.
First, a simple GUI shows up, in which you can see all your ongoing conversation.
When we click on the speak icon, it detects the voice and converts it to text using
speech_recognition module. 
On the text, first NLP is applied that creates a bag of words model which is then passed to a pre trained neural network made using the tflearn module. This network returns the "tag" with which 
the sentence is associated(see intents.json). 
This "tag" is then used to find the "sub tag" with which the sentence is associated
again with the help of the same model.
Once, the subtag is determined, it returns the appropriate answer associated with that
subtag, and the pyttsx3 module is used to convey the answer through voice.


