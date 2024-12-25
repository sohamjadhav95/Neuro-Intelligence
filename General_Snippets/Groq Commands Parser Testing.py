import re
import os
import datetime
from difflib import get_close_matches
from groq import Groq

# Automatically Initiating required envoirnmental variable
os.environ["GROQ_API_KEY"] = "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"

# Configure the Groq API with your API key
client = Groq(
    api_key=os.environ.get("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"),
)

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
    """
    Extract the command and argument from user input.
    """
    user_input = user_input.strip().lower()

    # Check if the command is one of the argumented commands
    for command in argumented_commands:
        if user_input.startswith(command):
            argument = user_input.replace(command, "").strip()
            return command, argument

    # Match the input to a general command
    closest_match = get_close_matches(user_input, general_commands, n=1, cutoff=0.6)
    if closest_match:
        command = closest_match[0]
        return command, ""

    # Fallback: Use Groq API for ambiguous input
    return get_command_from_groq(user_input)

# Function to get command from Groq API
def get_command_from_groq(user_input):
    """
    Use the Groq API to extract command and argument for ambiguous inputs.
    """
    prompt = (
        f"User input: {user_input}\n"
        f"Map the user input to one of the predefined commands: {', '.join(argumented_commands + general_commands)}.\n"
        f"Also extract the argument if present. Return the result in the format:\n"
        f"Command: <command>\nArgument: <argument>\n"
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    generated_text = response.choices[0].message.content.strip()
    match = re.search(r"Command: (.+)\nArgument: (.*)", generated_text)
    if match:
        command = match.group(1).strip()
        argument = match.group(2).strip()
        return command, argument
    else:
        return "Invalid command", ""

from difflib import SequenceMatcher

def test_accuracy(test_set):
    """
    Test the accuracy of command extraction and provide detailed metrics.
    """
    correct_predictions = 0
    detailed_results = []

    for user_input, expected_command, expected_argument in test_set:
        extracted_command, extracted_argument = extract_command_and_arguments(user_input)

        # Check command accuracy
        command_match = SequenceMatcher(None, extracted_command, expected_command).ratio()
        argument_match = SequenceMatcher(None, extracted_argument, expected_argument).ratio()

        is_correct = (
            command_match > 0.9 and
            (expected_argument == "" or argument_match > 0.9)  # Allow slight differences in arguments
        )
        if is_correct:
            correct_predictions += 1

        # Store detailed results
        detailed_results.append({
            "Input": user_input,
            "Expected Command": expected_command,
            "Extracted Command": extracted_command,
            "Expected Argument": expected_argument,
            "Extracted Argument": extracted_argument,
            "Command Match": command_match,
            "Argument Match": argument_match,
            "Correct": is_correct
        })

    accuracy = (correct_predictions / len(test_set)) * 100
    return accuracy, detailed_results

# Expanded test set
test_set = [
    ("Open the browser and search for AI tools", "open application", "browser and search for AI tools"),
    ("Close the notepad", "close application", "notepad"),
    ("Search for baby toys online", "web search", "baby toys online"),
    ("Look up Python tutorials on YouTube", "youtube search", "Python tutorials"),
    ("Click on the 'Start' menu", "click on", "'Start' menu"),
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
    ("Search for restaurants near me", "web search", "restaurants near me"),
    ("Play the latest music on YouTube", "youtube search", "latest music"),
    ("Snap the window to the left side", "snap window left", ""),
    ("What's the current date?", "current date", ""),
    ("Turn up the volume", "increase volume", ""),
    ("Unmute the sound", "unmute sound", ""),
    ("Check the email inbox", "check email", ""),
    ("Go to www.example.com", "open website", "www.example.com"),
    ("Restart the laptop", "restart", ""),
    ("Show me the system properties", "open system properties", "")
]

# Run accuracy testing
accuracy, results = test_accuracy(test_set)
print(f"Accuracy: {accuracy:.2f}%")
for result in results:
    print(result)
