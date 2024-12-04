from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the FLAN-T5 model and tokenizer
model_name = "google/flan-t5-base"  # You can upgrade to "flan-t5-large" if needed
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def extract_command(user_input, provided_commands):
    """
    Extract the command from the user input based on the provided list of commands.
    """
    commands_list = "\n".join([f"- {cmd}" for cmd in provided_commands])
    prompt = (
        f"You are a command extraction system. Extract the 'command' from the user input. "
        f"The command must match one of the following provided commands:\n{commands_list}\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def extract_argument(user_input):
    """
    Extract the argument from the user input, ignoring predefined commands.
    """
    prompt = (
        f"You are an argument extraction system. Extract the 'argument' from the user input, "
        f"which represents the specific name of application or a software.\n\n"
        f"Input: {user_input}\nOutput:"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def test_command_argument_extraction():
    """
    Test the functions for extracting command and argument separately.
    """
    # List of valid commands
    provided_commands = [
        "open application",
        "close application",
        "create file",
        "delete file"
    ]
    
    # User input for testing
    user_input = "please open the chrome app"
    
    # Extract command and argument separately
    extracted_command = extract_command(user_input, provided_commands)
    extracted_argument = extract_argument(user_input)
    
    # Print results
    print("User Input:", user_input)
    print("Extracted Command:", extracted_command)
    print("Extracted Argument:", extracted_argument)

# Run the test
test_command_argument_extraction()
