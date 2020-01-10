import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from subprocess import Popen , PIPE
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How may i help you?")
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query)
        return query

    except Exception as e:
        #print(e)
        print("Say that again please....")
        return "None"


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('pjava427@gmail.com', 'petals1@')
    server.sendmail('pjava427@gmail.com', to, content)
    server.close()

def execute_return(cmd):
    args = cmd.split()
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err

def make_req(error):
    resp = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle="+error+"&site=stackoverflow")
    return resp.json()

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count = count+1
        if count == 3 or count == len(i):
            break
    import webbrowser
    for i in url_list:
        webbrowser.open(i)



if __name__ == '__main__':
    wishMe()
    query="a"
    while query!="bye":
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching wikipedia....')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'find error' in query:
            speak("Which file should I inspect for errors?")
            a = takeCommand().lower()
            op, err = execute_return("python " + a + ".py")
            error_message = err.decode("utf-8").strip().split("\r\n")[-1]
            print(error_message)
            if error_message:
                filter_err = error_message.split(":")
                json1 = make_req(filter_err[0])
                json2 = make_req(filter_err[1])
                json = make_req(error_message)
                get_urls(json1)
                get_urls(json2)
                get_urls(json)
            else:
                speak("No Error")
                print("No Error")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("The time is"+ strTime)

        elif 'email to' in query:
            try:
                speak("What should i say")
                content = takeCommand()
                to = 'pvg2709@gmail.com'
                sendEmail(to, content)
                speak("Email sent")
            except Exception as e:
                speak("Sorry..can't send email")
        elif 'bye' in query:
            speak("Bye! see you again soon!")
