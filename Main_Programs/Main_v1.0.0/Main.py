# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import pyttsx3
import time

import speech_recognition as sr
from transformers import T5Tokenizer, T5ForConditionalGeneration

from Core_Commands import commands
from Core_Commands import execute_command

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
#-----------------------------------------------------------------------------------------------

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
            speak_text(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech API; {0}".format(e))
        
        
        
# Load the FLAN-T5 model and tokenizer
model_name = "google/flan-t5-base"  # You can upgrade to "flan-t5-large" if needed
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def extract_command(user_input):
    """
    Extract and normalize the command from the user input to match predefined commands.
    """
    prompt = (
        f"You are a command extraction system. Extract the 'command' from the user input "
        f"and ensure it matches one of the predefined commands: 'open application', 'close application'.\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    extracted_command = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Normalize the extracted command
    command_lower = extracted_command.lower()
    if "open" in command_lower or "launch" in command_lower or "start" in command_lower:
        return "open application"
    elif (
        "close" in command_lower
        or "shut down" in command_lower
        or "quit" in command_lower
        or "exit" in command_lower
    ):
        return "close application"
    else:
        return extracted_command  # Fallback to raw output if no match




def extract_argument(user_input):
    """
    Extract the argument from the user input, focusing on application names.
    Checks against a predefined list of application names first, then falls back to model extraction.
    """
    import re  # Use regex for better matching

    app_names = [
        "notepad", "calculator", "paint", "wordpad",
        "microsoft edge", "google chrome", "mozilla firefox",
        "microsoft word", "microsoft excel", "microsoft powerpoint",
        "vlc media player", "spotify", "adobe acrobat reader",
        "steam", "discord", "file explorer",
        "windows media player", "snipping tool", "task manager",
        "command prompt", "powershell", "control panel", "settings"]
    
    # Preprocess input for case-insensitive matching
    user_input_lower = user_input.lower()

    # Use regex to match predefined application names
    for app in app_names:
        if re.search(rf"\b{re.escape(app)}\b", user_input_lower):  # Ensure exact word match
            return app  # Return the matched application name

    # If no predefined app name is found, use the model to extract the argument
    prompt = (
        f"Extract the application or software name from the following user input. "
        f"Prioritize matching names from this predefined list: {', '.join(app_names)}. "
        f"If none match exactly, extract the most likely name mentioned in the input.\n\n"
        f"User Input: {user_input}\nApplication Name:"
    )

    # Generate model inputs and outputs
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def Command_Argument_Combined():
    
    user_input = listen_command()
    
    predicted_command = extract_command(user_input)
    predicted_argument = extract_argument(user_input)
    
    print (predicted_command +" "+ predicted_argument)
    return predicted_command +" "+ predicted_argument



#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

# Example loop to keep listening for commands
while True:
    command = Command_Argument_Combined()

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

            elif "create folder" in command:
                folder_name = command.replace("create folder ", "").strip()
                commands["create folder"](folder_name)

            elif "delete file" in command:
                file_name = command.replace("delete file ", "").strip()
                commands["delete file"](file_name)

            elif "move file" in command:
                parts = command.split(" to ")
                if len(parts) == 2:
                    file_name = parts[0].replace("move file ", "").strip()
                    destination = parts[1].strip()
                    commands["move file"](file_name, destination)

            elif "rename file" in command:
                parts = command.split(" to ")
                if len(parts) == 2:
                    old_name = parts[0].replace("rename file ", "").strip()
                    new_name = parts[1].strip()
                    commands["rename file"](old_name, new_name)

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