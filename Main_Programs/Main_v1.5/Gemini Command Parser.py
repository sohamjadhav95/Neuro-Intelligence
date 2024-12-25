import google.generativeai as genai
import re
from difflib import get_close_matches

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyAF8OCUS7KjTkCBRK6UojIWzdY0Ccah21Q")  # Replace with your API key

# Separate commands into general and argumented commands
argumented_commands = [
    "open application", "close application", "web search", "youtube search", "open website",
    "click on"
]

general_commands = [
    "battery status", "cpu usage", "internet status",
    "check email", "check internet", "get weather", "increase volume",
    "decrease volume", "mute sound", "unmute sound", "sleep mode",
    "shutdown", "restart", "current date", "current time",
    "close window", "minimize window", "maximize window", "switch window",
    "snap window left", "snap window right", "close all windows", "open new window",
    "minimize all windows", "restore window", "toggle taskbar visibility", "open task manager",
    "open file explorer", "open command prompt", "open browser", "open notepad",
    "open calculator", "open snipping tool", "open paint", "open wordpad",
    "open registry editor", "open disk management", "open device manager", "open event viewer",
    "take screenshot", "toggle full screen", "lock computer", "minimize all windows",
    "create virtual desktop", "switch virtual desktop", "open settings", "open update settings",
    "open sound settings", "open bluetooth settings", "open wifi settings", "open keyboard settings",
    "open mouse settings", "open display settings", "open language settings", "open time and date settings",
    "open taskbar settings", "open privacy settings", "open storage settings", "open apps settings",
    "open power and sleep settings", "open default apps settings", "open personalization settings", "open fonts settings",
    "open region settings", "open accounts settings", "open backup settings", "open security and maintenance",
    "open feedback hub", "open system properties", "open network connections", "open action center",
    "open device encryption settings", "open control panel", "open services"
]

# Function to extract command and arguments
def extract_command_and_arguments(user_input):
    # Normalize input
    user_input = user_input.strip().lower()
    
    # Check if the command is one of the argumented commands
    for command in argumented_commands:
        if user_input.startswith(command):
            # Extract the argument
            argument = user_input.replace(command, "").strip()
            return command, argument

    # Match the input to a general command
    closest_match = get_close_matches(user_input, general_commands, n=1, cutoff=0.6)
    if closest_match:
        command = closest_match[0]
        return command, ""
    
    # Fallback: Use Gemini to resolve ambiguous input
    return get_command_from_gemini(user_input)

# Function to get command from Gemini API
def get_command_from_gemini(user_input):
    prompt = (
        f"User input: {user_input}\n"
        f"Map the user input to one of the predefined commands: {', '.join(argumented_commands + general_commands)}.\n"
        f"Also extract the argument if present. Return the result in the format:\n"
        f"Command: <command>\nArgument: <argument>\n"
    )
    
    # Generate content using Gemini
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    # Parse Gemini response
    generated_text = response.text.strip()
    match = re.search(r"Command: (.+)\nArgument: (.*)", generated_text)
    if match:
        command = match.group(1).strip()
        argument = match.group(2).strip()
        return command, argument
    else:
        return "Invalid command", ""
    
    

# Large test set with expected outputs
test_set = [
    # Argumented commands
    ("Open the browser and search for AI tools", "open application", "browser and search for AI tools"),
    ("Close the notepad", "close application", "notepad"),
    ("Search for baby toys online", "web search", "baby toys online"),
    ("Look up Python tutorials on YouTube", "youtube search", "Python tutorials"),
    ("Click on the 'Start' menu", "click on", "'Start' menu"),

    # General commands
    ("Show me battery status", "battery status", ""),
    ("What is the CPU usage?", "cpu usage", ""),
    ("Check the internet status", "internet status", ""),
    ("Is the computer connected to the internet?", "check internet", ""),
    ("Give me the current weather", "get weather", ""),
    ("Mute the sound", "mute sound", ""),
    ("Increase the volume", "increase volume", ""),
    ("Shutdown the computer", "shutdown", ""),
    ("Restart the system", "restart", ""),
    ("Show me the current time", "current time", ""),
    ("Minimize all windows", "minimize all windows", ""),
    ("Take a screenshot of the screen", "take screenshot", ""),
    ("Lock the computer", "lock computer", ""),
    ("Switch to the next virtual desktop", "switch virtual desktop", ""),
    ("Open the settings", "open settings", ""),
]

# Function to process and print results for the test set
def process_test_set(test_set):
    for user_input, expected_command, expected_argument in test_set:
        command, argument = extract_command_and_arguments(user_input)
        print(f"Input: {user_input}")
        print(f"Extracted_Command: {command} {argument}")

# Run the function to process the test set
process_test_set(test_set)

