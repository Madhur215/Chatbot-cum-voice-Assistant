import numpy as np
import json
from model import create_model
import random
import tensorflow as tf
from prepare import prepare_data
import calender as cl
import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import tkinter as tk
import os
import webbrowser as wb
import threading
import weather
import wikipedia
import smtplib
import keys

try:
    from googlesearch import search
except:
    print("googlesearch not imported!")

SERVICE = cl.authenticate()

root = tk.Tk()
root.geometry('500x600')
heading = tk.Label(root, text="Welcome! Press the Button and ask whatever you want!",
                   font=('montserrat', 12, "bold"), fg="black").pack()
frame = tk.Frame(root, bg="#FFF")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
your_msg = tk.StringVar()
y_scroll_bar = tk.Scrollbar(frame)
x_scroll_bar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
msg_list = tk.Listbox(frame, height=20, width=50, yscrollcommand=y_scroll_bar.set, xscrollcommand=x_scroll_bar.set)
y_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.FALSE)
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
frame.pack()

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


tags = []  # Contains all the different tags
all_questions_list = []  # Contains the different question with their words tokenized
questions_tags = []  # Contains the questions tags corresponding to the questions in above list
all_question_words = []  # Contains all the words in all the questions of the dataset

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
    all_words_sub_questions, all_sub_tags, all_sub_questions_list, sub_question_tags = tr.prepare(intent, "sub_tags",
                                                                                                  "questions", "sub")

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


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def make_note():
    speak("What would you like me to write down? ")
    write = get_audio()
    note(write)
    speak("I've made a note of that.")
    msg_list.insert(tk.END, "Boss: I've made a note of that.")


def perform_google_search():
    speak("what would you like me to search for")
    query = get_audio()
    speak("I have the following results")
    msg_list.insert(tk.END, "Boss: I have the following results:")
    for result in search(query, tld="co.in", num=1, stop=1, pause=2):
        msg_list.insert(tk.END, "Boss: " + str(result))
        res = result

    wb.open(res)


def prepare_tags_list():
    for intent in data["intents"]:
        curr_tag = intent["tag"]
        s_tags_list = []
        for sub_tg in intent["sub_tags"]:
            curr_sub_tag = sub_tg["sub"]
            s_tags_list.append(curr_sub_tag)
            answers_dict[curr_sub_tag] = sub_tg["answers"]

        tags_dict[curr_tag] = s_tags_list


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Boss sir, How can I help you")




def send_mails(to, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(keys.EMAIL, keys.PASSWORD)
    server.sendmail('4as1827000224@gmail.com', to, body)
    server.close()


prepare_tags_list()


def main():
    sentence = get_audio()
    msg_list.insert(tk.END, "You: " + sentence)
    if sentence.count("exit") > 0:
        msg_list.insert(tk.END, "Boss: Good Bye!")
        speak("Good bye")
        root.quit()

    tag = model.predict_tag(sentence)
    sub = sub_tags_models[tag].predict_tag(sentence)
    tag_word = tags[tag]

    sub_list = tags_dict.get(tag_word)
    sub_tag_word = sub_list[sub]

    if sub_tag_word == "mails-send":
        try:
            speak("Who do you want to send this mail")
            to = get_audio()
            speak("what should I say to " + to)
            body = get_audio()
            send_mails(keys.DICT[to], body)
            speak("Your mail has been sent successfully !")
            msg_list.insert(tk.END, "Boss: Your mail has been sent successfully !")
        except Exception as e:
            print(e)
            speak("Sorry, Could not send this E-mail")
            msg_list.insert(tk.END, "Boss: Sorry, Could not send this E-mail")
    elif sub_tag_word == "wikipedia-open":
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        speak(a)
        results = wikipedia.summary(sentence, sentences=2)
        speak("According to wikipedia")
        speak(results)
        msg_list.insert(tk.END, "Boss: " + str(results))
    elif sub_tag_word == "music-open":
        path = keys.PATH_MUSIC
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        speak(a)
        os.startfile(path)
        msg_list.insert(tk.END, "Boss: opened Spotify")
    elif sub_tag_word == "visual-studio-code-open":
        path = keys.PATH_VS_CODE
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        speak(a)
        os.startfile(path)
        msg_list.insert(tk.END, "Boss: opened visual studio")
    elif sub_tag_word == "call-weather-api":
        speak("Please tell me the name of the city")
        city = get_audio()
        print("city: " + str(city))
        weather_conditions = weather.get_weather(str(city))
        speak(weather_conditions)
        msg_list.insert(tk.END, "Boss: " + str(weather_conditions))
    elif sub_tag_word == "know-date":
        date = cl.get_date_for_day(sentence)
        speak(date)
        msg_list.insert(tk.END, "Boss: " + str(date))

    elif sub_tag_word == "get-events":
        try:
            day = cl.get_date(sentence)
            cl.get_selected_events(SERVICE, day, msg_list, tk)
        except:
            speak("None")
            msg_list.insert(tk.END, "Boss: None")
    elif sub_tag_word == "all-events":
        try:
            cl.get_all_events(SERVICE, msg_list, tk)
        except:
            msg_list.insert(tk.END, "Boss: None")
            speak("None")
    elif sub_tag_word == "make-notes":
        try:
            make_note()
        except:
            msg_list.insert(tk.END, "Boss: Try again")
            speak("try again")
    elif sub_tag_word == "search-google":
        try:
            perform_google_search()
        except:
            msg_list.insert(tk.END, "Boss: An error occurred!")
            speak("An error occurred")
    else:
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        speak(a)
        msg_list.insert(tk.END, "Boss: " + str(a))


def run():
    main_thread = threading.Thread(target=main)
    main_thread.start()


picture = tk.PhotoImage(file=keys.PATH_IMAGE)
send_button = tk.Button(root, image=picture, command=run, borderwidth=0)
send_button.pack()

wish()

root.mainloop()
