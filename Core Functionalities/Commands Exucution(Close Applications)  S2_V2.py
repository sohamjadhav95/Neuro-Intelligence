# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import subprocess
import os

import speech_recognition as sr
import pyttsx3
import time
import psutil
import shutil

from pywinauto.application import Application
import pywinauto
import pygetwindow as gw

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set properties for TTS engine (optional)
tts_engine.setProperty('rate', 200)  # Speed of speech
tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Function to speak text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    time.sleep(1)  # Short delay after speaking


# Open applications

def open_application(app_name):
    """
    Attempts to open an application using Windows Start Menu search and pywinauto as a fallback.
    """
    # Try to open via Start Menu
    try:
        subprocess.run(f"start {app_name}", check=True, shell=True)
        speak_text(f"Opening {app_name}")
        speak_text(f"{app_name} Opened") 
        return True
    except Exception:
        speak_text(f"Could not open {app_name} via Start Menu. Trying another method...")

    # If Start Menu search fails, try using pywinauto
    try:
        Application().start(app_name)  # Attempt to start the application by name
        speak_text(f"Opening {app_name} using pywinauto.")
        speak_text(f"{app_name} Opened") 
        return True
    except Exception:
        speak_text(f"Sorry, I don't know how to open {app_name}. Ensure it's installed and accessible.")
        return False
    
       
def open_application_fallback(app_name):
    """
    Attempts to open an application by checking a predefined dictionary and the system PATH.
    If unsuccessful, returns False to indicate further methods should be attempted.
    """
    # Apps dictionery
    apps = {
        "chrome": "chrome",
        "notepad": "notepad",
        "calculator": "calculator",
        "firefox": "firefox",
        "file explorer": "explorer",
        "command prompt": "cmd",
        "calculator": "calc",

    }
    # Check if the app is available in the system PATH
    app_path = shutil.which(app_name.lower())
    
    # Check if the app is in the predefined dictionary
    if app_name.lower() in apps:
        app_command = apps[app_name.lower()]
        try:
            speak_text(f"Opening {app_name}...")
            subprocess.Popen([app_command])
            speak_text(f"{app_name} Opened") 
            return True
        except FileNotFoundError:
            speak_text(f"Error: Could not open {app_name}. Trying another method...")
            return False  # Proceed to fallback method if the app fails to open
    
    
    # Check and execute the app path instead of app name
    elif app_path:
        speak_text(f"Opening {app_name}...")
        try:
            subprocess.Popen([app_path])  # Open the application using its path
            return True
        except FileNotFoundError:
            speak_text(f"Error: Could not open {app_name}.")
            return False
    
    # If neither dictionary nor PATH yielded results, return False
    return False     

      
# Close applictions

def close_application(app_name):
    # Try to use pygetwindow first
    try:
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            for window in windows:
                window.close()  # Close the window
            speak_text(f"Closing {app_name} using Window...")
        else:
            speak_text(f"Could not find {app_name} window with window.")
    
    # If pygetwindow fails, try pywinauto
    except Exception as e:
        speak_text(f"Error closing {app_name} with pygetwindow: {e}")
        
        try:
            app = pywinauto.Application().connect(title_re=app_name, timeout=5)
            app.kill()  # Force kill the app
            speak_text(f"Closing {app_name} using pywinauto...")
        except Exception as e:
            speak_text(f"Error closing {app_name} with pywinauto: {e}")
            
            # If pywinauto also fails, fall back to taskkill
            try:
                subprocess.run(f"taskkill /f /im {app_name}.exe", check=True, shell=True)
                speak_text(f"Forcefully closing {app_name} using taskkill...")
            except subprocess.CalledProcessError:
                speak_text(f"Error: Could not close {app_name} using taskkill.")


# Basic Commands

commands = {
    "exit": lambda: speak_text("Exiting, Good bye!"),
    
    # Application Control
    "open application": lambda app_name: open_application(app_name),
    "close application": lambda app_name: close_application(app_name),

    # File and Folder Management
    "create folder": lambda folder_name: speak_text(f"Creating folder named {folder_name}..."),  # Add folder creation code here
    "delete file": lambda file_name: speak_text(f"Deleting file named {file_name}..."),  # Add file deletion code here
    "move file": lambda file_name, destination: speak_text(f"Moving {file_name} to {destination}..."),  # Add file moving code here
    "rename file": lambda old_name, new_name: speak_text(f"Renaming {old_name} to {new_name}..."),  # Add renaming code here

    # System Information
    "battery status": lambda: speak_text("Checking battery status..."),  # Add battery check code here
    "cpu usage": lambda: speak_text("Fetching CPU usage..."),  # Add CPU usage check code here
    "internet status": lambda: speak_text("Checking internet connection..."),  # Add internet check code here
    "current time": lambda: speak_text(f"The current time is {time.strftime('%I:%M %p')}."),

    # Web and Browser Commands
    "web search": lambda query: speak_text(f"Searching the web for {query}..."),  # Add web search code here
    "youtube search": lambda query: speak_text(f"Searching YouTube for {query}..."),  # Add YouTube search code here
    "check email": lambda: speak_text("Opening email client..."),  # Add email client opening code here

    # System Control
    "increase volume": lambda: speak_text("Increasing volume..."),  # Add volume increase code here
    "decrease volume": lambda: speak_text("Decreasing volume..."),  # Add volume decrease code here
    "mute sound": lambda: speak_text("Muting sound..."),  # Add muting code here
    "unmute sound": lambda: speak_text("Unmuting sound..."),  # Add unmuting code here
    "sleep mode": lambda: speak_text("Putting computer to sleep..."),  # Add sleep mode code here
    "shutdown": lambda: speak_text("Shutting down the system..."),  # Add shutdown code here
    "restart": lambda: speak_text("Restarting the system..."),  # Add restart code here

    # Personal Assistant
    "set reminder": lambda reminder: speak_text(f"Setting reminder: {reminder}"),  # Add reminder setting code here
    "tell joke": lambda: speak_text("Why don't scientists trust atoms? Because they make up everything!"),
    "current date": lambda: speak_text(f"Today’s date is {time.strftime('%B %d, %Y')}."),

    # Automation and Scripting
    "run script": lambda script_name: speak_text(f"Running script {script_name}..."),  # Add script running code here
    "open favorite": lambda doc_name: speak_text(f"Opening {doc_name}..."),  # Add favorite document opening code here
}

#-----------------------------------------------------------------------------------------------

# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)

        try:
            # Recognize and print command
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            speak_text(f"You said: {command}")
            return command.lower()

        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak_text("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("Network error.")
            speak_text("Network error.")
            return None

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

        # Check if the command exists in the dictionary and execute it
        elif command in commands:
            # Execute the command using the lambda function in the dictionary
            commands[command]()
        
        # Handle commands that require additional input
        elif "open application" in command:
            app_name = command.replace("open application ", "").strip()
            if not open_application(app_name):
                open_application_fallback(app_name)
          
        # Close application command
        elif "close application" in command:
            app_name = command.replace("close application ", "").strip()
            commands["close application"](app_name)
        
        elif "set reminder" in command:
            reminder_text = command.replace("set reminder ", "")
            commands["set reminder"](reminder_text)

        elif "web search" in command:
            search_query = command.replace("web search ", "")
            commands["web search"](search_query)

        elif "youtube search" in command:
            youtube_query = command.replace("youtube search ", "")
            commands["youtube search"](youtube_query)
        
        # If command not recognized
        else:
            speak_text("Command not recognized.")


