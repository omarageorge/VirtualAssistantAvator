import asyncio
import speech_recognition as sr
from gtts import gTTS
import playsound as pl
import os
from datetime import date, datetime, time
import python_weather
import warnings
import wikipedia
import webbrowser
import platform
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
    
    # Keeps the soundEngine active
    while True:
            
        # Get sound input from microphone
        command = soundEngine()
        
        if 'good morning' or 'good afternoon' or 'good evening' in command:  # Greetings Handler
            if isMorning():
                speechEngine('good morning!')
            elif isAfterNoon():
                speechEngine('good afternoon!')
            elif isEvening():
                speechEngine('good evening!')
                
        elif 'hello' in command:  # Hello Handler
            speechEngine('Hello!')
        
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
                
        elif 'goodbye' in command:     # Exit Handler
            # Goodbye response
            speechEngine('Have a nice time, Goodbye!')
            # Exit application
            break    
        else:
            pass
        

# Main function
def main():
    # Run command processor
    commandProcessor()

# Calling Main function
if __name__ == '__main__':
    main()
