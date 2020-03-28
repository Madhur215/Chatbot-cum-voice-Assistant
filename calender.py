from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz
import pyttsx3
import speech_recognition as sr


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "febraury", "march", "april", "may", "june", "july", "august", "september"
			,"october", "november", "december"]
DAYS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
DAY_EXTENTIONS = ["st", "nd", "th", "rd"]
MONTH_DAYS = {0:31, 1:28, 2:31, 3:30, 4: 31, 5: 30,
			 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}

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

def get_date(text):
	today = datetime.date.today()
	text = text.lower()
	if text.count("today") > 0:
		return today
	
	if text.count("tommorrow") > 0:
		today += datetime.timedelta(days=1)
		return today

	day = -1
	day_of_week = -1
	month = -1
	year = today.year

	for word in text.split():
		if word in MONTHS:
			month = MONTHS.index(word) + 1
		elif word in DAYS:
			day_of_week = DAYS.index(word)
		elif word.isdigit():
			day = int(word)
		else:
			for ext in DAY_EXTENTIONS:
				found = word.find(ext)
				if found > 0:
					try:
						day = int(word[:found])
					except:
						pass

	if month < today.month and month != -1:
		year = year+1

	if month == -1 and day != -1: 
		if day < today.day:
			month = today.month + 1
		else:
			month = today.month

	if month == -1 and day == -1 and day_of_week != -1:
		current_day_of_week = today.weekday()
		dif = day_of_week - current_day_of_week

		if dif < 0:
			dif += 7
			if text.count("next") >= 1:
				dif += 7

		return today + datetime.timedelta(dif)

	if day != -1:
		return datetime.date(month=month, day=day, year=year)

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

    # Call the Calendar API

def get_all_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=20, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_selected_events(service, day):
	date = datetime.datetime.combine(day, datetime.datetime.min.time())
	end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
	utc = pytz.UTC
	date = date.astimezone(utc)
	end_date = end_date.astimezone(utc)

	events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
										singleEvents=True,orderBy='startTime').execute()
	events = events_result.get('items', [])

	if not events:
		speak('No events found!')
	else:
		speak(f"You have {len(events)} events on this day.")

		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			print(start, event['summary'])
			start_time = str(start.split("T")[1].split("-")[0])
			if int(start_time.split(":")[0]) < 12:
				start_time = start_time + "am"
			else:
				start_time = str(int(start_time.split(":")[0])-12)
				start_time = start_time + "pm"

			speak(event["summary"] + " at " + start_time)

def get_date_for_day(text):
	text = text.lower()
	today = datetime.date.today()

	if text.count("today") > 0:
		return today.weekday()
	if text.count("tomorrow") > 0:
		today += datetime.timedelta(days=1)
		return today

	for word in text.split():
		if word in DAYS:
			# TODO just get the date
			required_day = DAYS.index(word)
			diff = required_day - today.weekday() + 1
			if diff < 0:
				diff += 7
				if text.count("next") >= 1:
					diff += 7

			curr_month = today.month
			day = today.day + diff
			if day > MONTH_DAYS.get(curr_month):
				day -= MONTH_DAYS.get(curr_month)
				curr_month = today.month - 1 
			year = today.year
			return datetime.date(month=curr_month, day=day, year=year)












