<<<<<<< HEAD
=======
import speech_recognition as sr
from gtts import gTTS
import playsound as pl
import os
import datetime
import warnings
import calendar
import random
import wikipedia


#ignore any warnings messages
warnings.filterwarnings('ignore')


# Listen to commands
def listener():
    
    # Create a listener object
    listener = sr.Recognizer()
    
    # Listen to sound from microphone
    with sr.Microphone() as source:
        
        # Show microphone status
        print('Listening...')
        
        # Store data received from microphone
        microphone_data = listener.listen(source)
        
        # Stores text data from conversion
        sound_to_text = ''
        
        try:
            # Convert microphone data to text
            sound_to_text = listener.recognize_google(microphone_data)
        except:
            print('Sorry, I did not get that!')
        
        return sound_to_text
        
        

# Speech
def speechEngine(text):
    
    # Sound file name
    sound_file = 'voice_audio_file.mp3'
    
    # Check is Voice audio file already exists
    if os.path.isfile(sound_file):
        os.remove(sound_file)
    
    # Convert text to speech
    soundObject = gTTS(text, lang='en', slow=False)
    
    # Save sound_file to file system
    soundObject.save(sound_file)
    
    # Talk
    pl.playsound(sound_file)
    
>>>>>>> dev
