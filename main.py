import asyncio
import speech_recognition as sr
from gtts import gTTS
import playsound as pl
import os
from datetime import date, datetime, time
import python_weather
import warnings
import wikipedia


#ignore any warnings messages
warnings.filterwarnings('ignore')


# Listen to commands
def soundEngine():
    
    # Create a listener object
    listener = sr.Recognizer()
    
    # Listen to sound from microphone
    with sr.Microphone() as source:
        
        # Show microphone status
        print('Listening...')
        
        # Store data received from microphone
        microphone_data = listener.listen(source)
        
        # Covert to lowercase
        microphone_data
        
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
def commandEngine():
    while True:
            
        # Load output from microphone
        command = soundEngine()
        
        # command = 'gye'
        
        
    
        if 'goodbye' in command:     # Exit Handler
            speechEngine('Have a nice time, Goodbye!')
            break
        
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
            location = 'greenland'
            
            # Weather finder
            async def getWeather(location):
                # Declare the client
                client = python_weather.Client(format=python_weather.IMPERIAL)
                weather =  await client.find(location)
                return weather.current.temperature
                await client.close()
            
            # Get weather    
            weather = asyncio.run(getWeather(location))
            
            # convert weather to Fahrenheit
            weather_in_celsius = (weather - 32) * (5/9)
            
            # Format weather output
            weather_response = f'The weather is {round(weather_in_celsius, 1)} degrees celsius'
            
            # Render response
            speechEngine(weather_response)
            
    else:
        pass
        




# Main function
def main():
    commandEngine()


# Execute main function 
if __name__ == '__main__':
    main()
