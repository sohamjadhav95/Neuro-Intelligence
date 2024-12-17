import time
import csv
import pyttsx3

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




# --*Main Code of Basic Commands*--

commands = {
    "exit": lambda: speak_text("Exiting, Good bye!"),
    
    # UI Access (Click on elements)
    "click on": lambda element_name: ui_handler.click_on(element_name),
    
    # System Information
    "battery status": lambda: system_information.get_battery_status(),
    "cpu usage": lambda: system_information.get_cpu_usage(),
    "internet status": lambda: system_information.check_internet(),
    "current time": lambda: system_information.get_current_time(),
    
    # Web and Browser Commands
    "check email": lambda: web_functions.check_email(),
    "check internet": lambda: web_functions.check_internet(),
    "get weather": lambda city_name: web_functions.get_weather(city_name),
  
    # System Control
    "increase volume": lambda: system_control.increase_volume(),
    "decrease volume": lambda: system_control.decrease_volume(),
    "mute sound": lambda: system_control.mute_sound(),
    "unmute sound": lambda: system_control.unmute_sound(),
    "sleep mode": lambda: system_control.sleep_mode(),
    "shutdown": lambda: system_control.shutdown(),
    "restart": lambda: system_control.restart(),
    
    # Personal Assistant
    "set reminder": lambda reminder: speak_text(f"Setting reminder: {reminder}"),  # Add reminder setting code here
    "tell joke": lambda: speak_text("Why don't scientists trust atoms? Because they make up everything!"),
    "current date": lambda: speak_text(f"Today’s date is {time.strftime('%B %d, %Y')}."),

    # Automation and Scripting
    "run script": lambda script_name: speak_text(f"Running script {script_name}..."),  # Add script running code here
    "open favorite": lambda doc_name: speak_text(f"Opening {doc_name}..."),  # Add favorite document opening code here
}