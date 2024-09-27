import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "6ba772e955814570a7565300e8dd9a7d"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    

    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running while the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiprocess(command):
    client = OpenAI(api_key="sk-proj-eY1aIKbkK8N0dPSCgLF4T3BlbkFJEbMTMeHNsFb95avpNSeD",
    )


    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant name john, skilled in explaining complex programming concepts with creative flair, give short responses and always start the sentence with cheem tapak dum dum"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content



def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        webbrowser.open(musiclibrary.music[song])
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=6ba772e955814570a7565300e8dd9a7d")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        #Let openAi handle the request
        output = aiprocess(c)
        speak(output)        
     
if __name__ == "__main__":
    speak("Initialising john....")
    while True:
        #Listen for the wake word "chotu"
        #obtain audio from microphone
        r = sr.Recognizer()
        


        print("Recognizing...")
    
    


        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2,phrase_time_limit=1)

            word = r.recognize_google(audio)
            if (word.lower() == "john"):
                 speak("cheem tapak dum dum")

                 #Listen for command
                 with sr.Microphone() as source:
                    print("john activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)


                    processcommand(command)

        except Exception as e:
                print("Error; {0}".format(e))
            



