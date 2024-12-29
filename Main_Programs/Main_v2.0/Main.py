# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import pyttsx3
import time

import speech_recognition as sr

from Core_Commands import commands

from Dynamic_Commands_Exucution import Gemini_Input
from Groq_Commands_Parser import extract_command_and_arguments ,get_command_from_groq
from Core_Functions import listen_command, listen_for_trigger, speak_text

# In CoreCommands.py
from Core_Functions import ApplicationHandler, WebFunctions

# Instantiate where needed:
app_handler = ApplicationHandler()
web_functions = WebFunctions()


#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Main loop
trigger_words = ["hey google", "hey listen", "how are you"]  # Define trigger words

while True:
    # Listen for a trigger word
    trigger_command = listen_for_trigger()
    
    if any(trigger in trigger_command for trigger in trigger_words):
        print("Trigger word detected. Listening for commands...")
        main_command = listen_command(timeout=10)

        if main_command:
            # Exit command to stop the loop
            if "exit" in main_command:
                commands["exit"]()
                break

            # Process main command
            try:
                extracted_command, argument = extract_command_and_arguments(main_command)

                if not extracted_command or extracted_command == "Invalid command":
                    speak_text("Command is complex or not trained, using another approach.")
                    speak_text("Performing Operation...")
                    Gemini_Input(main_command)
                    continue

                # Execute commands
                if extracted_command in commands:
                    if argument:
                        commands[extracted_command](argument)
                    else:
                        commands[extracted_command]()

                elif "click on" in extracted_command:
                    commands["click on"](argument)

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

                else:
                    speak_text("Performing Operation...")
                    Gemini_Input(main_command)

            except KeyError as e:
                speak_text(f"Command key error: {str(e)}. Please try again.")
            except TypeError as e:
                speak_text(f"Type error occurred: {str(e)}. Please check your command format.")
            except Exception as e:
                speak_text(f"An error occurred: {str(e)}. Please try again.")

