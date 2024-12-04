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
        
    # Application Control
    "open application": lambda app_name: app_handler.open_application(app_name),
    "close application": lambda app_name: app_handler.close_application(app_name),

    # File and Folder Management
    "create folder": lambda folder_name: file_handler.create_folder(folder_name),
    "delete file": lambda file_name: file_handler.delete_file(file_name),
    "move file": lambda file_name, destination: file_handler.move_file(file_name, destination),
    "rename file": lambda old_name, new_name: file_handler.rename_file(old_name, new_name),
    
    # System Information
    "battery status": lambda: system_information.get_battery_status(),
    "cpu usage": lambda: system_information.get_cpu_usage(),
    "internet status": lambda: system_information.check_internet(),
    "current time": lambda: system_information.get_current_time(),
    
    # Web and Browser Commands
    "web search": lambda query: web_functions.web_search(query),
    "youtube search": lambda query: web_functions.youtube_search(query),
    "check email": lambda: web_functions.check_email(),
    "check internet": lambda: web_functions.check_internet(),
    "get weather": lambda city_name: web_functions.get_weather(city_name),
    "open website": lambda website_url: web_functions.open_website(website_url),
  
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



# Commands Data

def load_command_mapping(csv_file):
    command_mapping = {}
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip comment lines starting with #
            if row['keyword'].startswith('#'):
                continue
            trigger = row['keyword'].strip()  # Changed from 'Trigger Word(s)'
            command = row['command'].strip()  # Changed from 'Command'
            command_mapping[trigger] = command
    return command_mapping

# Load the command mapping
csv_file = "E:\Projects\VoxSys\Main Programs\command_mapping.csv"
command_mapping = load_command_mapping(csv_file)



def execute_command(user_input):
    """
    Analyze user input, map keywords to commands, and extract arguments.
    """
    # Normalize user input (case-insensitive matching)
    user_input = user_input.lower()

    # Find the keyword in the user input
    for keyword, command in command_mapping.items():
        if user_input.startswith(keyword):
            # Map keyword to command and extract argument
            argument = user_input[len(keyword):].strip()

            # Combine command and argument
            full_command = f"{command} {argument}"
            
            print(f"Predicted Command: {full_command}")
            
            return full_command

    # If no match is found
    print("No matching command found.")
    return None
