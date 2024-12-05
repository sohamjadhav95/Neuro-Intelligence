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

    
def test_accuracy(test_data):
    """
    Test the model's accuracy for command and argument extraction.

    Parameters:
    - test_data: A list of dictionaries containing user_input, expected_command, and expected_argument.

    Returns:
    - A dictionary with accuracy percentages for commands and arguments.
    """
    correct_commands = 0
    correct_arguments = 0

    for data in test_data:
        user_input = data["user_input"]
        expected_command = data["expected_command"]
        expected_argument = data["expected_argument"]

        # Extract the predicted command and argument
        predicted_command = extract_command(user_input)
        predicted_argument = extract_argument(user_input)

        # Compare predictions with expected values
        if predicted_command == expected_command:
            correct_commands += 1
        if predicted_argument.lower() == expected_argument.lower():  # Case-insensitive comparison
            correct_arguments += 1

        # Print individual results
        print(f"User Input: {user_input}")
        print(f"Expected Command: {expected_command}, Predicted Command: {predicted_command}")
        print(f"Expected Argument: {expected_argument}, Predicted Argument: {predicted_argument}")
        print("--------------------------------------------------")

    # Calculate accuracy
    command_accuracy = (correct_commands / len(test_data)) * 100
    argument_accuracy = (correct_arguments / len(test_data)) * 100

    # Print summary
    print(f"Command Accuracy: {command_accuracy:.2f}%")
    print(f"Argument Accuracy: {argument_accuracy:.2f}%")

    return {"command_accuracy": command_accuracy, "argument_accuracy": argument_accuracy}


test_data = [
    {"user_input": "please open the notepad", "expected_command": "open application", "expected_argument": "notepad"},
    {"user_input": "launch google chrome", "expected_command": "open application", "expected_argument": "google chrome"},
    {"user_input": "close the VLC media player", "expected_command": "close application", "expected_argument": "vlc media player"},
    {"user_input": "exit from task manager", "expected_command": "close application", "expected_argument": "task manager"},
    {"user_input": "start mozilla firefox", "expected_command": "open application", "expected_argument": "mozilla firefox"},
    {"user_input": "open microsoft word", "expected_command": "open application", "expected_argument": "microsoft word"},
    {"user_input": "close microsoft excel", "expected_command": "close application", "expected_argument": "microsoft excel"},
    {"user_input": "launch spotify", "expected_command": "open application", "expected_argument": "spotify"},
    {"user_input": "quit paint", "expected_command": "close application", "expected_argument": "paint"},
    {"user_input": "open command prompt", "expected_command": "open application", "expected_argument": "command prompt"},
    {"user_input": "close microsoft powerpoint", "expected_command": "close application", "expected_argument": "microsoft powerpoint"},
    {"user_input": "launch adobe acrobat reader", "expected_command": "open application", "expected_argument": "adobe acrobat reader"},
    {"user_input": "quit file explorer", "expected_command": "close application", "expected_argument": "file explorer"},
    {"user_input": "start task manager", "expected_command": "open application", "expected_argument": "task manager"},
    {"user_input": "open settings", "expected_command": "open application", "expected_argument": "settings"},
    {"user_input": "close snipping tool", "expected_command": "close application", "expected_argument": "snipping tool"},
    {"user_input": "launch steam", "expected_command": "open application", "expected_argument": "steam"},
    {"user_input": "open microsoft edge", "expected_command": "open application", "expected_argument": "microsoft edge"},
    {"user_input": "close windows media player", "expected_command": "close application", "expected_argument": "windows media player"},
    {"user_input": "start powershell", "expected_command": "open application", "expected_argument": "powershell"},
    {"user_input": "quit calculator", "expected_command": "close application", "expected_argument": "calculator"},
    {"user_input": "open wordpad", "expected_command": "open application", "expected_argument": "wordpad"},
    {"user_input": "launch control panel", "expected_command": "open application", "expected_argument": "control panel"},
    {"user_input": "close discord", "expected_command": "close application", "expected_argument": "discord"},
    {"user_input": "start vlc media player", "expected_command": "open application", "expected_argument": "vlc media player"},
    {"user_input": "quit spotify", "expected_command": "close application", "expected_argument": "spotify"},
    {"user_input": "open calculator", "expected_command": "open application", "expected_argument": "calculator"},
    {"user_input": "close microsoft edge", "expected_command": "close application", "expected_argument": "microsoft edge"},
    {"user_input": "launch paint", "expected_command": "open application", "expected_argument": "paint"},
    {"user_input": "quit microsoft word", "expected_command": "close application", "expected_argument": "microsoft word"},
    {"user_input": "open snipping tool", "expected_command": "open application", "expected_argument": "snipping tool"},
    {"user_input": "launch command prompt", "expected_command": "open application", "expected_argument": "command prompt"},
    {"user_input": "close google chrome", "expected_command": "close application", "expected_argument": "google chrome"},
    {"user_input": "start adobe acrobat reader", "expected_command": "open application", "expected_argument": "adobe acrobat reader"},
    {"user_input": "quit file explorer", "expected_command": "close application", "expected_argument": "file explorer"},
    {"user_input": "open vlc media player", "expected_command": "open application", "expected_argument": "vlc media player"},
    {"user_input": "close microsoft powerpoint", "expected_command": "close application", "expected_argument": "microsoft powerpoint"},
    {"user_input": "launch steam", "expected_command": "open application", "expected_argument": "steam"},
    {"user_input": "quit microsoft excel", "expected_command": "close application", "expected_argument": "microsoft excel"},
    {"user_input": "start microsoft edge", "expected_command": "open application", "expected_argument": "microsoft edge"},
    {"user_input": "open control panel", "expected_command": "open application", "expected_argument": "control panel"},
    {"user_input": "close discord", "expected_command": "close application", "expected_argument": "discord"},
    {"user_input": "launch powershell", "expected_command": "open application", "expected_argument": "powershell"},
    {"user_input": "quit spotify", "expected_command": "close application", "expected_argument": "spotify"},
    {"user_input": "start notepad", "expected_command": "open application", "expected_argument": "notepad"},
    {"user_input": "close calculator", "expected_command": "close application", "expected_argument": "calculator"},
    {"user_input": "launch task manager", "expected_command": "open application", "expected_argument": "task manager"},
    {"user_input": "quit microsoft word", "expected_command": "close application", "expected_argument": "microsoft word"},
    {"user_input": "open microsoft excel", "expected_command": "open application", "expected_argument": "microsoft excel"},
    {"user_input": "start windows media player", "expected_command": "open application", "expected_argument": "windows media player"},
    {"user_input": "close microsoft edge", "expected_command": "close application", "expected_argument": "microsoft edge"},
    {"user_input": "launch file explorer", "expected_command": "open application", "expected_argument": "file explorer"},
    {"user_input": "quit adobe acrobat reader", "expected_command": "close application", "expected_argument": "adobe acrobat reader"},
    {"user_input": "open vlc media player", "expected_command": "open application", "expected_argument": "vlc media player"},
    {"user_input": "close mozilla firefox", "expected_command": "close application", "expected_argument": "mozilla firefox"},
    {"user_input": "launch microsoft powerpoint", "expected_command": "open application", "expected_argument": "microsoft powerpoint"},
    {"user_input": "quit snipping tool", "expected_command": "close application", "expected_argument": "snipping tool"},
    {"user_input": "start paint", "expected_command": "open application", "expected_argument": "paint"},
    {"user_input": "close wordpad", "expected_command": "close application", "expected_argument": "wordpad"},
    {"user_input": "launch settings", "expected_command": "open application", "expected_argument": "settings"},
    {"user_input": "open microsoft word", "expected_command": "open application", "expected_argument": "microsoft word"},
    {"user_input": "start discord", "expected_command": "open application", "expected_argument": "discord"},
    # Add more to reach 100 commands
]


results = test_accuracy(test_data)
print(f"Final Results: {results}")
