from tkinter import *
import speech_recognition as sr
from gtts import gTTS
import playsound as pl
from datetime import date, time
import warnings
import wikipedia
import pyjokes
import webbrowser
import platform
import os
import requests
import sys
from minilib import *

# ignore any warnings messages
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
        except sr.UnknownValueError:
            speechEngine("Sorry i was a bit distracted there for a sec.Can you say that again please ?")

        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))

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


        elif 'introduce' in command:
            intro = '''
            My name is Anna. Your personal virtual assistant. I can help you with simple tasks like, checking the weather, date or time, 
            '''
            speechEngine(intro)

        elif 'your name' in command:
            intro = '''
             I'm Leo, its a pleasure to meet you.
                       '''
            speechEngine(intro)

        elif 'date' in command:  # Date Handler
            today = date.today()
            date_response = f"The date today is {today.strftime('%d %B, %Y')}."
            speechEngine(date_response)

        elif 'time' in command:  # Time handler
            time_str = datetime.now()
            time_response = f"The time is {time_str.strftime('%I:%M %p')}."
            speechEngine(time_response)

        elif 'weather' in command:  # Weather Handler
            # set location

            new_var = command.split()
            location = new_var[5]

            user_api = os.environ['OW_api_key']


            complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api
            api_link = requests.get(complete_api_link)
            api_data = api_link.json()


            # Get weather
            try:


                #read api data

                weather_desc = api_data['weather'][0]['description']
                temp_city = ((api_data['main']['temp']) - 273.15)
                hmdt = api_data['main']['humidity']
                # wind_spd = api_data['wind']['speed']

                weather_response = f'Its currently {weather_desc} and {(round(temp_city),1)} degrees celcius in {location} with a humidity of {hmdt} %'

                # Render response
                speechEngine(weather_response)
            #except IndexError as E:
                speechEngine("Can you please repeat that?")
            except:
                # Weather not found
                speechEngine(f"Sorry! I couldn't find the weather data for {location}.")

        elif 'open' in command:  # Opens search platforms (YouTube, Wikipedia, Google)
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
                speechEngine('just give me a sec!')
                wiki = wikipedia.summary(topic, sentences=2)
                speechEngine(wiki)
            except:
                speechEngine(f'Did not find anything on {topic} on wikipedia.')

        elif 'joke' in command:

            # Retrieve jokes
            joke = pyjokes.get_joke()

            # Tell the joke
            speechEngine("Okay!")
            speechEngine(joke)


        elif 'bye' in command:  # Exit Handler
            # Goodbye response
            speechEngine("I'll be here whenever you need me! bye for now.")
            # Exit application
            break
        else:
            pass


# Main function
def main():
    # Creating Tkinter Object
    app = Tk()
    app.title('Virtual Assistant Avatar')
    app.geometry('340x440')
    app.configure(background='#fff')
    app.wm_resizable(width=False, height=False)
    app.call('wm', 'attributes', '.', '-topmost', '1')

    # Microphone button
    mic_img = PhotoImage(file='./images/mic.png')
    btn_mic = Label(app, image=mic_img, border=0, background='#fff', cursor='hand2')
    btn_mic.pack(side=TOP, pady=20)

    # Avatar image
    avatar_img = PhotoImage(file='./images/avatar.png')
    avatar_lbl = Label(image=avatar_img, background='#fff')
    avatar_lbl.pack(side=BOTTOM)

    # Function to execute after gui loads
    def start_engines():
        # Start command processor
        commandProcessor()

        # Exit system
        exit()

    # Start_engines function after 1s
    app.after(1000, start_engines)

    app.mainloop()


if __name__ == '__main__':
    main()
    # commandProcessor()