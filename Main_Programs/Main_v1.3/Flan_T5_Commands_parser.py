from transformers import T5Tokenizer, T5ForConditionalGeneration
from difflib import get_close_matches

# Load the FLAN-T5 model and tokenizer
model_name = "google/flan-t5-large"  # You can upgrade to "flan-t5-large" if needed
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# List of predefined commands and their arguments
command_list = [
    "open application", "close application", "web search", "youtube search", "open website",
    "click on", "battery status", "cpu usage", "internet status",
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

def extract_command(user_input):
    """
    Extract and normalize the command from the user input to match predefined commands.
    """
    prompt = (
        f"You are a command extraction system. Extract the 'command' from the user input "
        f"and ensure it matches one of the predefined commands: {', '.join(command_list)}.\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    extracted_command = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()

    # Use fuzzy matching to find the closest predefined command
    matched_command = get_close_matches(extracted_command, command_list, n=1, cutoff=0.6)
    
    # Return the matched command or the user input if no match is found
    return matched_command[0] if matched_command else user_input

def extract_argument(user_input):
    """
    Extract the argument (such as application name or website) from the user input.
    """
    # Predefined list of application names
    app_names = [
        "notepad", "calculator", "paint", "wordpad",
        "microsoft edge", "google chrome", "mozilla firefox",
        "microsoft word", "microsoft excel", "microsoft powerpoint",
        "vlc media player", "spotify", "adobe acrobat reader",
        "steam", "discord", "file explorer",
        "windows media player", "snipping tool", "task manager",
        "command prompt", "powershell", "control panel", "settings"
    ]

    # Check for predefined app names in the user input
    for app in app_names:
        if app in user_input.lower():
            return app  # Return the matched application name

    # If no predefined app name is found, use the model to extract the argument
    prompt = (
        f"You are an argument extraction system. Extract the 'argument' from the user input, "
        f"which represents the specific name of an application or software in the provided list.\n\n"
        f"If application or software name does not match from list, you can extract the specific argument that is mentioned in the user input.\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

def process_input(user_input):
    """
    Process the user input to extract command and argument.
    """
    predicted_command = extract_command(user_input)
    predicted_argument = extract_argument(user_input)
    
    print(f"Command: {predicted_command}\nArgument: {predicted_argument}")
    return predicted_command, predicted_argument

# Example usage
if __name__ == "__main__":
    # Sample user inputs to test
    test_inputs = [
        "Can you open Notepad?",
        "Close the Spotify app.",
        "Search for climate change on the web.",
        "Go to www.example.com.",
        "Play some songs."
        "Launch the Calculator."
        "Please open Paint."
        "Mute the system volume."
        "Search Google for AI advancements."
        "Take a screenshot now."
        "Launch the Calculator."
        "Please open Paint."
        "Mute the system volume."
        "Search Google for AI advancements."
        "Take a screenshot now."
        "Open the Notepad."
        "Close all windows on my screen."
        "Check the weather forecast for tomorrow."
        "Increase the volume by 10 percent."
        "Minimize all the windows."
    ]
    
    for user_input in test_inputs:
        print(f"Input: {user_input}")
        process_input(user_input)
        print("-" * 40)
