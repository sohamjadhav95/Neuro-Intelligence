# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import subprocess
import os

import speech_recognition as sr
import pygetwindow as gw
import pyttsx3
import time
import psutil
import shutil
import pywinauto

from pywinauto.application import Application
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



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

# *Open applications*

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

      
# *Close applictions*

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


# *System Control Functions*

# Increase Volume
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.1, 1.0)  # Increase by 10%, max is 1
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak_text(f"Volume increased to {int(new_volume * 100)}%.")

# Decrease Volume
def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.1, 0.0)  # Decrease by 10%, min is 0
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak_text(f"Volume decreased to {int(new_volume * 100)}%.")

# Mute Sound
def mute_sound():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(True, None)
    speak_text("Sound muted.")

# Unmute Sound
def unmute_sound():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(False, None)
    speak_text("Sound unmuted.")

# Sleep Mode
def sleep_mode():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    speak_text("System is going to sleep mode.")

# Shutdown with confirmation
def shutdown():
    speak_text("Are you sure you want to shut down the system? Say 'yes' to proceed or 'no' to cancel.")
    confirmation = listen_command()  # Listen for the user's confirmation

    if confirmation is not None:
        if "yes" in confirmation:
            speak_text("Shutting down the system.")
            os.system("shutdown /s /t 1")  # Shutdown immediately
        elif "no" in confirmation:
            speak_text("Shutdown cancelled.")
        else:
            speak_text("Sorry, I didn't catch that. Please say 'yes' or 'no'.")

# Restart with confirmation
def restart():
    speak_text("Are you sure you want to restart the system? Say 'yes' to proceed or 'no' to cancel.")
    confirmation = listen_command()  # Listen for the user's confirmation

    if confirmation is not None:
        if "yes" in confirmation:
            speak_text("Restarting the system.")
            os.system("shutdown /r /t 1")  # Restart immediately
        elif "no" in confirmation:
            speak_text("Restart cancelled.")
        else:
            speak_text("Sorry, I didn't catch that. Please say 'yes' or 'no'.")

    
    
# *System Infromation Functions*

# Battery Status
def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plug_status = "plugged in" if battery.power_plugged else "not plugged in"
        speak_text(f"Battery is at {percent}% and is {plug_status}.")
    else:
        speak_text("Unable to fetch battery status.")

# CPU Usage
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)  # Interval gives a more accurate reading
    speak_text(f"Current CPU usage is {cpu_percent}%.")
    
# Internet Status
def check_internet():
    try:
        subprocess.run(["ping", "8.8.8.8", "-n", "1"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        speak_text("Internet is connected.")
    except subprocess.CalledProcessError:
        speak_text("No internet connection detected.")

# Current Time
def get_current_time():
    speak_text(f"The current time is {time.strftime('%I:%M %p')}.")


# *File Operations*

# 1. Define File Handling Functions
def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
        speak_text(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        speak_text(f"Folder '{folder_name}' already exists.")
    except Exception as e:
        speak_text(f"An error occurred: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        speak_text(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        speak_text(f"File '{file_path}' not found.")
    except Exception as e:
        speak_text(f"An error occurred: {e}")

def move_file(file_path, destination_folder):
    try:
        shutil.move(file_path, destination_folder)
        speak_text(f"Moved '{file_path}' to '{destination_folder}'.")
    except FileNotFoundError:
        speak_text(f"File '{file_path}' or destination '{destination_folder}' not found.")
    except Exception as e:
        speak_text(f"An error occurred: {e}")

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        speak_text(f"Renamed '{old_name}' to '{new_name}'.")
    except FileNotFoundError:
        speak_text(f"File '{old_name}' not found.")
    except Exception as e:
        speak_text(f"An error occurred: {e}")





# Basic Commands

commands = {
    "exit": lambda: speak_text("Exiting, Good bye!"),
    
    # Application Control
    "open application": lambda app_name: open_application(app_name),
    "close application": lambda app_name: close_application(app_name),

    # File and Folder Management
    "create folder": lambda folder_name: create_folder(folder_name),
    "delete file": lambda file_name: delete_file(file_name),
    "move file": lambda file_name, destination: move_file(file_name, destination),
    "rename file": lambda old_name, new_name: rename_file(old_name, new_name),
    
    # System Information
    "battery status": lambda: get_battery_status(),
    "cpu usage": lambda: get_cpu_usage(),
    "internet status": lambda: check_internet(),
    "current time": lambda: get_current_time(),
    
    # Web and Browser Commands
    "web search": lambda query: speak_text(f"Searching the web for {query}..."),  # Add web search code here
    "youtube search": lambda query: speak_text(f"Searching YouTube for {query}..."),  # Add YouTube search code here
    "check email": lambda: speak_text("Opening email client..."),  # Add email client opening code here

    # System Control
    "increase volume": lambda: increase_volume(),
    "decrease volume": lambda: decrease_volume(),
    "mute sound": lambda: mute_sound(),
    "unmute sound": lambda: unmute_sound(),
    "sleep mode": lambda: sleep_mode(),
    "shutdown": lambda: shutdown(),
    "restart": lambda: restart(),
    
    # Personal Assistant
    "set reminder": lambda reminder: speak_text(f"Setting reminder: {reminder}"),  # Add reminder setting code here
    "tell joke": lambda: speak_text("Why don't scientists trust atoms? Because they make up everything!"),
    "current date": lambda: speak_text(f"Today’s date is {time.strftime('%B %d, %Y')}."),

    # Automation and Scripting
    "run script": lambda script_name: speak_text(f"Running script {script_name}..."),  # Add script running code here
    "open favorite": lambda doc_name: speak_text(f"Opening {doc_name}..."),  # Add favorite document opening code here
}

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
  #----------------------------------------------------------------------------  
        # Handle commands that require additional input
        elif "open application" in command:
            app_name = command.replace("open application ", "").strip()
            if not open_application(app_name):
                open_application_fallback(app_name)
          
        # Close application command
        elif "close application" in command:
            app_name = command.replace("close application ", "").strip()
            commands["close application"](app_name)
  #----------------------------------------------------------------------------         
        elif "set reminder" in command:
            reminder_text = command.replace("set reminder ", "")
            commands["set reminder"](reminder_text)

        elif "web search" in command:
            search_query = command.replace("web search ", "")
            commands["web search"](search_query)

        elif "youtube search" in command:
            youtube_query = command.replace("youtube search ", "")
            commands["youtube search"](youtube_query)
 #----------------------------------------------------------------------------           
        # In the main loop after capturing File/ Folder handling commands
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
#-------------------------------------------------------------------------------
        
        # If command not recognized
        else:
            speak_text("Command not recognized.")


