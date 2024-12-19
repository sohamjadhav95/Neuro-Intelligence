# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import pyttsx3
import time

import speech_recognition as sr

from Core_Commands import commands

# In CoreCommands.py
from Core_Functions import ApplicationHandler, System_control, SystemInfromation, FileHandler, WebFunctions
from Core_Functions import WebFunctions, UIHandler

# Instantiate where needed:
app_handler = ApplicationHandler()
system_control = System_control()
system_information = SystemInfromation()  # Consider renaming this to SystemInformation if needed
file_handler = FileHandler()
web_functions = WebFunctions()
ui_handler = UIHandler()


# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init('sapi5')

# Set properties for TTS engine (optional)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voices', voices[0].id) # Voice for chat
tts_engine.setProperty('rate', 200)  # Speed of speech
tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Function to speak text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    time.sleep(1)  # Short delay after speaking

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def listen_command():
    with sr.Microphone() as source:
        try:
            print("Calibrating for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate for 1 second
            print("Listening... Please speak clearly.")
            
            # Use a timeout for responsiveness
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            
            # Text-to-speech feedback (optional)
            speak_text(f"You said: {command}")
            return command.lower()
        
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio. Please try again.")
        except sr.WaitTimeoutError:
            print("No speech detected. Please speak louder or closer to the microphone.")
        except sr.RequestError as e:
            print(f"Google Speech API error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return None  # Return None if no valid command is captured




#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Example loop to keep listening for commands
while True:
    command = "open region settings"

    if command:
        # Exit command to stop the loop
        if "exit" in command:
            commands["exit"]()
            break

        try:
            # Default command execution
            if command in commands:
                commands[command]()
            
            # Handle "click on" command
            elif "click on" in command:
                element_name = command.replace("click on ", "").strip()
                commands["click on"](element_name)

            # Commands requiring additional input
            elif "open application" in command:
                app_name = command.replace("open application ", "").strip()
                if not app_handler.open_application(app_name):
                    app_handler.open_application_fallback(app_name)

            elif "close application" in command:
                app_name = command.replace("close application ", "").strip()
                app_handler.close_application(app_name)

            elif "set reminder" in command:
                reminder_text = command.replace("set reminder ", "")
                commands["set reminder"](reminder_text)

            elif "web search" in command:
                search_query = command.replace("web search ", "")
                commands["web search"](search_query)

            elif "youtube search" in command:
                youtube_query = command.replace("youtube search ", "")
                commands["youtube search"](youtube_query)

            elif "open website" in command:
                website_url = command.replace("open website ", "").strip()
                web_functions.open_website(website_url)

            # Command not recognized
            else:
                speak_text("Command not recognized.")

        except KeyError as e:
            speak_text(f"Command key error: {str(e)}. Please try again.")
        except TypeError as e:
            speak_text(f"Type error occurred: {str(e)}. Please check your command format.")
        except Exception as e:
            speak_text(f"An error occurred: {str(e)}. Please try again.")