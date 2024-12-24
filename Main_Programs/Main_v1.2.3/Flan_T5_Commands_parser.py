from transformers import T5Tokenizer, T5ForConditionalGeneration
from difflib import get_close_matches

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
        f"and ensure it must match one of the predefined commands: 'open application', 'close application', 'web search', 'youtube search', 'open website', 'click on' "
        f"Once command match from user input return the predifined command as it is."
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    extracted_command = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()

    return extracted_command

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
        f"which represents the specific name of an application, software, website name in the provided list.\n\n"
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
        "open chrome app now"
    ]
    
    for user_input in test_inputs:
        print(f"Input: {user_input}")
        process_input(user_input)
        print("-" * 40)
