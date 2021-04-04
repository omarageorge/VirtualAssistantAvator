import speech_recognition as sr
from gtts import gTTS
import playsound as pl
import os
import datetime
import warnings
import calendar
import random
import wikipedia

listener = sr.Recognizer()
        

def receive_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
    except sr.UnknownValueError:
        pass
        
