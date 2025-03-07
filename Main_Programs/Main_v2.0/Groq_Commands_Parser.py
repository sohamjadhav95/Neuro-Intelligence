import re
import os
from groq import Groq

# Automatically Initiating required environmental variable
os.environ["GROQ_API_KEY"] = "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"

# Configure the Groq API with your API key
client = Groq(
    api_key=os.environ.get("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"),
)

# Predefined commands
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


def get_command_from_groq(user_input):
    word_count = len(user_input.split())  # Count words correctly
    
    if word_count > 5:
        return user_input  # Return input as is if word count > 5
    else:
        # Generate the Groq API prompt
        prompt = (
            f"User input: {user_input}\n"
            f"Map the user input to one of the predefined commands: {', '.join(argumented_commands + general_commands)}.\n"
            f"Also extract the argument if present. Return the result in the format:\n"
            f"Command: <command>\nArgument: <argument>\n"
        )

        # Call the Groq API
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
        except Exception as e:
            print(f"Error with Groq API: {e}")
            return "Invalid command"

        # Parse the response
        generated_text = response.choices[0].message.content.strip()
        match = re.search(r"Command: (.+)\nArgument: (.*)", generated_text)

        if match:
            command = match.group(1).strip()
            argument = match.group(2).strip()

            # Validate against predefined commands
            all_commands = [cmd.lower() for cmd in argumented_commands + general_commands]
            if command.lower() not in all_commands:
                return "Invalid command"

            # Clean up "None" values in command or argument
            if command.lower() == "none":
                command = ""
            if argument.lower() == "none":
                argument = ""

            result = f"{command} {argument}".strip()  # Concatenate and strip extra spaces
            print(result)
            return result
        else:
            print(f"Unexpected Groq API response: {generated_text}")
            return "Invalid command"
