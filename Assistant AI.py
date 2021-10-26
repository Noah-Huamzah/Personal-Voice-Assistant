import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pywhatkit
import wolframalpha
import json
import requests
import math

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good Morning')
    elif 12 <= hour < 18:
        speak('Good Afternoon')
    else:
        speak('Good Evening')


def acceptCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.adjust_for_ambient_noise(source, 1)
        command_audio = r.listen(source, timeout=3)
        try:
            query = r.recognize_google(command_audio, language='en-in')
            print(query)
        except Exception as e:
            print(e)
            print('Speech Incomprehensible')
            return "None"
        return query


if __name__ == '__main__':
    wish()
    speak("How may I help you. To ask specific questions, say ask questions first")
    while True:
        query = acceptCommand().lower()
        if 'wikipedia' in query or 'who is' in query or 'what is' in query:
            speak('Searching Wikipedia')
            query = query.replace('wikipedia', '')
            query = query.replace('who is', '')
            query = query.replace('what is', '')
            query = query.replace('when is', '')
            query = query.replace(' ', '_')
            result = wikipedia.summary(query, 2)
            print(result)
            speak(result)

        elif 'open youtube' in query:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')))
            webbrowser.get('chrome').open('https://www.youtube.com/')

        elif 'my playlist' in query:
            speak('Playing from your playlist')
            music_dir = ''
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'play' in query:
            speak('On it')
            query = query.replace('play', '')
            pywhatkit.playonyt(query)

        elif 'time' in query:
            currentTime = datetime.datetime.now().strftime('%H:%M')
            speak(f'The time is {currentTime}')

        elif 'search' in query or 'when is' in query:
            query = query.replace('search ', '')
            query = query.replace(' ', '+')
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')))
            webbrowser.get('chrome').open('https://www.google.com/search?q=' + query)

        elif 'ask questions' in query:
            speak('What do want to ask')
            question = acceptCommand()
            app_id = '8KTKHJ-38R9VPVJL7'
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            for i in res.results:
                print(i.text)
                speak(i.text)

        elif 'weather' in query:
            api_key = '3e202d5c53cf135e743496c295cfd643'
            base_url = 'https://api.openweathermap.org/data/2.5/weather?q='
            speak('Please specify the city name again')
            city_name = acceptCommand()
            city_name = city_name.replace(' ', '%20')
            complete_url = base_url + city_name + '&appid=' + api_key
            response = requests.get(complete_url)
            x = response.json()
            if x['cod'] != '404':
                y = x['main']
                current_temp = y['temp']
                temp_C = math.ceil(current_temp - 273)
                print(temp_C)
                speak(temp_C)
                speak('degree celsius')

        elif 'exit' in query:
            speak('Have a nice day. Bye')
            quit()
