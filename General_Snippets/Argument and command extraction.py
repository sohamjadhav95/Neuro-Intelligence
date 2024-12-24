from transformers import T5Tokenizer, T5ForConditionalGeneration
from difflib import get_close_matches

def map_to_command(user_input):
    # Initialize the tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    # Define the list of exact commands
    exact_commands = [
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

    # Create the input prompt for the model
    prompt = (
        f"Map the user command to EXACTLY one of these commands: {', '.join(exact_commands)}. "
        f"User input: {user_input}. Your response must match one command from the list exactly."
    )

    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate the output with controlled decoding
    outputs = model.generate(
        **inputs,
        max_length=32,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    # Decode the generated output
    mapped_command = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()

    # Validate the mapped command
    closest_match = get_close_matches(mapped_command, exact_commands, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        # Suggest the closest possible command or fallback
        partial_matches = get_close_matches(mapped_command, exact_commands, n=3, cutoff=0.3)
        if partial_matches in exact_commands:
            return f"Closest match: {partial_matches[0]}"
        else:
            return "Invalid output: command not recognized."


def evaluate_accuracy():
    test_cases = [
        {"input": "What is the current status of my battery?", "expected": "battery status"},
        {"input": "Show me CPU usage", "expected": "cpu usage"},
        {"input": "Is the internet working?", "expected": "internet status"},
        {"input": "Increase the sound volume", "expected": "increase volume"},
        {"input": "Shut down the system", "expected": "shutdown"},
        {"input": "What time is it?", "expected": "current time"},
        {"input": "Minimize all the windows", "expected": "minimize all windows"},
        {"input": "Mute the sound", "expected": "mute sound"},
        {"input": "Unmute the sound", "expected": "unmute sound"},
        {"input": "Switch to the next virtual desktop", "expected": "switch virtual desktop"},
        {"input": "Take a screenshot", "expected": "take screenshot"},
        {"input": "Open the file explorer", "expected": "open file explorer"},
        {"input": "Restart the system", "expected": "restart"},
        {"input": "Show me the task manager", "expected": "open task manager"},
        {"input": "Lock my computer", "expected": "lock computer"},
        {"input": "Snap the window to the left", "expected": "snap window left"},
        {"input": "Maximize this window", "expected": "maximize window"}
    ]

    correct = 0
    total = len(test_cases)

    for case in test_cases:
        user_input = case["input"]
        expected = case["expected"]
        predicted = map_to_command(user_input)
        
        print(f"Input: {user_input}")
        print(f"Expected: {expected}")
        print(f"Predicted: {predicted}\n")

        if predicted.strip().lower() == expected.strip().lower():
            correct += 1

    accuracy = (correct / total) * 100
    print(f"Accuracy: {accuracy:.2f}%")

# Example usage
evaluate_accuracy()
