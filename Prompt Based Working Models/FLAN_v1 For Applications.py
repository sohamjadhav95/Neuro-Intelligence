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
    import re  # Use regex for better matching

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

    # Preprocess input for case-insensitive matching
    user_input_lower = user_input.lower()

    # Use regex to match predefined application names
    for app in app_names:
        if re.search(rf"\b{re.escape(app)}\b", user_input_lower):  # Ensure exact word match
            return app  # Return the matched application name

    # If no predefined app name is found, use the model to extract the argument
    prompt = (
        f"Extract the application or software name from the following user input. "
        f"Prioritize matching names from this predefined list: {', '.join(app_names)}. "
        f"If none match exactly, extract the most likely name mentioned in the input.\n\n"
        f"User Input: {user_input}\nApplication Name:"
    )

    # Generate model inputs and outputs
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)



def Command_Argument_Combined():
    predicted_command = extract_command(user_input)
    predicted_argument = extract_argument(user_input)
    
    print (predicted_command +" "+ predicted_argument)
    return predicted_command +" "+ predicted_argument


user_input = "open chrome"

Command_Argument_Combined()