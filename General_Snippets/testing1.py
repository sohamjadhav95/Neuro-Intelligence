from difflib import get_close_matches

# Predefined lists
command_list = [
    "open application", "close application", "web search", "youtube search", "open website",
    "click on", "battery status", "cpu usage", "internet status", "check email",
    "get weather", "increase volume", "decrease volume", "mute sound", "unmute sound",
    "sleep mode", "shutdown", "restart", "current date", "current time", "close window"
]

app_names = [
    "notepad", "calculator", "paint", "wordpad", "spotify", "chrome", "firefox", "vlc", "task manager", "command prompt"
]

# Preprocess input
def preprocess_input(user_input):
    unnecessary_words = ["please", "kindly", "could you", "can you", "now", "for me"]
    for word in unnecessary_words:
        user_input = user_input.lower().replace(word, "")
    return user_input.strip()

# Match commands
def extract_command(user_input):
    user_input = preprocess_input(user_input)
    closest_match = get_close_matches(user_input, command_list, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else "unknown command"

# Match arguments
def extract_argument(user_input):
    user_input = preprocess_input(user_input)
    for app in app_names:
        if app in user_input:
            return app
    return "unknown argument"

# Main function
def process_input(user_input):
    predicted_command = extract_command(user_input)
    predicted_argument = extract_argument(user_input)
    print(f"Command: {predicted_command}\nArgument: {predicted_argument}")
    return predicted_command, predicted_argument

# Test cases
def test_accuracy():
    test_cases = [
        ("open calculator", "open application", "calculator"),
        ("please launch paint", "open application", "paint"),
        ("could you open the task manager for me?", "open application", "task manager"),
        ("opne calclator", "open application", "calculator"),
        ("open Spotify now", "open application", "spotify"),
        ("What's the weather like today?", "get weather", "weather"),
        ("turn off all the sound", "mute sound", "sound"),
    ]

    correct_predictions = 0

    for user_input, expected_command, expected_argument in test_cases:
        predicted_command, predicted_argument = process_input(user_input)
        is_command_correct = predicted_command == expected_command
        is_argument_correct = predicted_argument == expected_argument

        if is_command_correct and is_argument_correct:
            correct_predictions += 1
        else:
            print(f"Test Failed for Input: '{user_input}'")
            print(f"Expected Command: {expected_command}, Predicted Command: {predicted_command}")
            print(f"Expected Argument: {expected_argument}, Predicted Argument: {predicted_argument}")
            print("---")

    accuracy = (correct_predictions / len(test_cases)) * 100
    print(f"Accuracy: {accuracy:.2f}% ({correct_predictions}/{len(test_cases)})")

# Run test
test_accuracy()
