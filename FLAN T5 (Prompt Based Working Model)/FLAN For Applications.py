from transformers import T5Tokenizer, T5ForConditionalGeneration

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
    # List of predefined application names
    app_names = [
        "notepad",
        "calculator",
        "paint",
        "wordpad",
        "microsoft edge",
        "google chrome",
        "mozilla firefox",
        "microsoft word",
        "microsoft excel",
        "microsoft powerpoint",
        "vlc media player",
        "spotify",
        "adobe acrobat reader",
        "steam",
        "discord",
        "file explorer",
        "windows media player",
        "snipping tool",
        "task manager",
        "command prompt",
        "powershell",
        "control panel",
        "settings"
    ]
    
    # Check for predefined app names in the user input
    for app in app_names:
        if app in user_input.lower():
            return app  # Return the matched application name
    
    # If no predefined app name is found, use the model to extract the argument
    prompt = (
        f"You are an argument extraction system. Extract the 'argument' from the user input, "
        f"which represents the specific name of application or a software in the provided list.\n\n"
        f"If application or software name not match from list then you can extract the specific name that are mentioned in user input.\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def test_command_argument_extraction():
    """
    Test the functions for extracting command and argument with multiple user inputs.
    """
    
    # User inputs for testing
    user_inputs = [
        "please open the notepad",
        "launch google chrome",
        "close the VLC media player",
        "can you open the calculator",
        "shut down the Spotify app",
        "please close the Zoom app",
        "launch the command prompt",
        "open Adobe Acrobat Reader",
        "close the steam application",
        "please open microsoft word",
        "exit from task manager",
        "launch microsoft excel",
        "quit the paint application",
        "start mozilla firefox"
    ]
    
    # Iterate over each user input
    for user_input in user_inputs:
        # Extract command and argument separately
        extracted_command = extract_command(user_input)
        extracted_argument = extract_argument(user_input)
        
        # Print results
        print("User Input:", user_input)
        print("Extracted Command:", extracted_command)
        print("Extracted Argument:", extracted_argument)
        print("-" * 50)

# Run the test
test_command_argument_extraction()

