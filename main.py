from tkinter import *
import speech_recognition as sr
from gtts import gTTS
import playsound as pl
from datetime import date, datetime, time
import python_weather
import warnings
import wikipedia
import webbrowser
import platform
import asyncio
import os
from minilib import isMorning, isAfterNoon, isEvening



#ignore any warnings messages
warnings.filterwarnings('ignore')

# Listens to commands
def soundEngine():
    
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
            pass
        
        return sound_to_text.lower()
        
        
# Speech Handler
def speechEngine(text):
    
    # Sound file name
    sound_file = 'voice_audio_file.mp3'
    
    # Convert text to speech
    soundObject = gTTS(text, lang='en', slow=False)
    
    # Save sound_file to file system
    soundObject.save(sound_file)
    
    # Talk
    pl.playsound(sound_file)
    
    # Cleanup
    if os.path.isfile(sound_file):
        os.remove(sound_file)
    
    
# Handles commands passed into the system
def commandProcessor():
    
    # Respond to salutations
    def respond_to_greeting():
        if isMorning():
            speechEngine('good morning!')
        elif isAfterNoon():
            speechEngine('good afternoon!')
        elif isEvening():
            speechEngine('good evening!')

    # Keeps the soundEngine active
    while True:
            
        # Get sound input from microphone
        command = soundEngine()
        print(command)
        
        if 'good morning' in command:  # Good morning
            respond_to_greeting()
        
        elif 'good afternoon' in command:  # Good afternoon
            respond_to_greeting()
        
        elif 'good evening' in command:  # Good evening
            respond_to_greeting()
                
        elif 'hello' in command:  # Hello Handler
            speechEngine('Hi how are you?')
        
        elif 'date' in command: # Date Handler
            today = date.today()
            date_response = f"The date today is {today.strftime('%d %B, %Y')}."
            speechEngine(date_response)
            
        elif 'time' in command: # Time handler
            time_str = datetime.now()
            time_response = f"The time is {time_str.strftime('%I:%M %p')}."
            speechEngine(time_response)
            
        elif 'weather' in command:  # Weather Handler
            # set location
            location = 'kampala'
            
            # Weather finder
            async def getWeather(location):
                # Declare the client
                client = python_weather.Client(format=python_weather.IMPERIAL)
                weather =  await client.find(location)
                return weather.current.temperature
                await client.close()
            
            # Get weather    
            try:
                weather = asyncio.run(getWeather(location))
            
                # convert weather to Celsius
                weather_in_celsius = (weather - 32) * (5/9)
            
                # Format weather output
                weather_response = f'The weather is {round(weather_in_celsius, 1)} degrees celsius'
            
                # Render response
                speechEngine(weather_response)
            except:
                # Weather not found
                speechEngine(f"Sorry! I couldn't find the weather data for {location}.")
                
        elif 'search' in command:  # Opens search platforms (YouTube, Wikipedia, Google)
            if 'youtube' in command:  # Opens YouTube
                speechEngine('Opening youtube!')
                webbrowser.open_new_tab('https://www.youtube.com/')
                
            elif 'wikipedia' in command:  # Opens Wikipedia
                speechEngine('Opening wikipedia!')
                webbrowser.open_new_tab('https://www.wikipedia.org/')
                
            else:  # Opens Google Search
                speechEngine('Opening google search!')
                webbrowser.open_new_tab('https://google.com/')
        
        elif 'google' in command:
            
            # Remove the google word from command
            filtered = command.replace('google', '')
            
            # Remove extra spaces from start and end of the query
            search_query = filtered.strip()
            
            # Form google search query string
            query_string = f'https://www.google.com/search?&client={platform.system}&q={search_query}'
            
            # Voice response
            speechEngine(f'googling {search_query}')
            
            # Open web browser on a new tab
            webbrowser.open_new_tab(query_string)
        
        elif 'email' in command:
            speechEngine('Opening emails')
            webbrowser.open_new_tab('https://mail.google.com/mail')
                
        elif 'tell me about' in command:
            replaced = command.replace('tell me about', '')
            topic = replaced.strip()
            try:
                wiki = wikipedia.summary(topic, sentences=2)
                speechEngine(wiki)
            except:
                speechEngine(f'Did not find anything on {topic} on wikipedia.')
                
            
        elif 'bye' in command:     # Exit Handler
            # Goodbye response
            speechEngine("I'l be here whenever you need me! bye for now.")
            # Exit application
            break    
        else:
            pass





# GLOBALS
ACTIVE_STATUS = False  # Stores soundEngine active status

def main():

    # Status event manager
    def manage_status(event):
        global ACTIVE_STATUS
        ACTIVE_STATUS = not ACTIVE_STATUS
        
        if ACTIVE_STATUS:
            app.title('Listening...')
            # commandProcessor()
        else:
            app.title('Sleeping...')
            

    app = Tk(className='Virtual Assistant Avator')
    app.geometry('340x440')
    app.configure(background='#fff')
    app.wm_resizable(width=False, height=False)
    


    # Micropone button
    mic_img = PhotoImage(file='./images/mic.png')
    btn_mic = Button(app, image=mic_img, borderwidth=0, activebackground='#f38a8e' ,background='#fff', cursor='hand2')
    btn_mic.bind('<Button-1>', manage_status)
    btn_mic.pack(side=TOP, pady=20)

    # Avator image
    avator_img = PhotoImage(file='./images/avator.png')
    avator_lbl = Label(image=avator_img, background='#fff')
    avator_lbl.pack(side=BOTTOM)

    app.mainloop()



if __name__ == '__main__':
    # main()
    commandProcessor()