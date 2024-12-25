# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import pyttsx3
import time

import speech_recognition as sr

from Core_Commands import commands

from Dynamic_Commands_Exucution import Gemini_Input
from Groq_Commands_Parser import extract_command_and_arguments ,get_command_from_groq

# In CoreCommands.py
from Core_Functions import ApplicationHandler, WebFunctions

# Instantiate where needed:
app_handler = ApplicationHandler()
web_functions = WebFunctions()



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

# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            # Using Google Speech API (no large models to download)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech API; {0}".format(e))



#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Example loop to keep listening for commands
while True:
    command = listen_command()

    if command:
        # Exit command to stop the loop
        if "exit" in command:
            commands["exit"]()
            break

        try:
            # Extract command and arguments using get_command_from_groq
            extracted_command, argument = extract_command_and_arguments(command)

            # Check for invalid or blank commands
            if not extracted_command or extracted_command == "Invalid command":
                speak_text("Invalid command or no input detected. Please try again.")
                speak_text("Performing Operation...")
                Gemini_Input(command)
                continue

            # Default command execution
            if extracted_command in commands:
                if argument:
                    commands[extracted_command](argument)
                else:
                    commands[extracted_command]()

            # Handle "click on" command
            elif "click on" in extracted_command:
                commands["click on"](argument)

            # Commands requiring additional input
            elif extracted_command == "open application":
                if not app_handler.open_application(argument):
                    app_handler.open_application_fallback(argument)

            elif extracted_command == "close application":
                app_handler.close_application(argument)

            elif extracted_command == "web search":
                commands["web search"](argument)

            elif extracted_command == "youtube search":
                commands["youtube search"](argument)

            elif extracted_command == "open website":
                web_functions.open_website(argument)

            # Command not recognized
            else:
                speak_text("Performing Operation...")
                Gemini_Input(command)

        except KeyError as e:
            speak_text(f"Command key error: {str(e)}. Please try again.")
        except TypeError as e:
            speak_text(f"Type error occurred: {str(e)}. Please check your command format.")
        except Exception as e:
            speak_text(f"An error occurred: {str(e)}. Please try again.")

