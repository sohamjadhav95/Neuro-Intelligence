import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Load Dataset
df = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Simplified model Tested (99% accurate)\natural_language_commands_cleaned.csv")


# Preprocess
df['natural_language_command'] = df['natural_language_command'].str.lower()

# Encode Target Labels
le_main_command = LabelEncoder()
df['main_command_label'] = le_main_command.fit_transform(df['main_command'])

le_argument = LabelEncoder()
df['argument_label'] = le_argument.fit_transform(df['argument'])

# Split Data
X = df['natural_language_command']
y_main_command = df['main_command_label']
y_argument = df['argument_label']

X_train, X_test, y_main_train, y_main_test = train_test_split(
    X, y_main_command, test_size=0.15, random_state=42
)
_, _, y_arg_train, y_arg_test = train_test_split(
    X, y_argument, test_size=0.15, random_state=42
)

# Vectorize Text
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Main Command Model
main_model = SVC(kernel='linear', random_state=42)
main_model.fit(X_train_vec, y_main_train)

# Train Argument Model
arg_model = SVC(kernel='linear', random_state=42)
arg_model.fit(X_train_vec, y_arg_train)

# Function to Predict Both
def predict_main_and_argument(input_text):
    input_text = input_text.lower()
    input_vec = vectorizer.transform([input_text])

    # Predict Main Command
    main_pred = main_model.predict(input_vec)
    main_command = le_main_command.inverse_transform(main_pred)[0]

    # Predict Argument
    arg_pred = arg_model.predict(input_vec)
    argument = le_argument.inverse_transform(arg_pred)[0]

    full_command = f"{main_command} {argument}"
    print(full_command)
    return main_command, argument


# Real examples for testing
test_examples = [
    ("can you show me battery status", "system_status", "battery"),
    ("help me check memory usage", "system_status", "memory usage"),
    ("please open calculator", "open_application", "calculator"),
    ("find tutorials for programming", "web_search", "tutorials"),
    ("terminate firefox now", "close_application", "firefox"),
    ("can you open chrome for me", "open_application", "chrome"),
    ("launch spotify, please", "open_application", "spotify"),
    ("start notepad", "open_application", "notepad"),
    ("close PowerPoint now", "close_application", "powerpoint"),
    ("shut down Excel", "close_application", "excel"),
    ("terminate Firefox", "close_application", "firefox"),
    ("turn the volume up", "media_control", "volume up"),
    ("can you mute the sound", "media_control", "mute"),
    ("please unmute the audio", "media_control", "unmute"),
    ("what's my battery status", "system_status", "battery"),
    ("check the CPU usage", "system_status", "cpu usage"),
    ("tell me about the internet connection", "system_status", "network status"),
    ("search for Python tutorials online", "web_search", "tutorials"),
    ("can you find some restaurants nearby", "web_search", "restaurants"),
    ("look up the weather forecast for New York", "web_search", "weather forecast"),
]

# Initialize counters for correct predictions
correct_main_cmd = 0
correct_arg = 0

# Total examples
total_examples = len(test_examples)

# Evaluate each example
for example, true_main_cmd, true_arg in test_examples:
    predicted_main_cmd, predicted_arg = predict_main_and_argument(example)
    print(f"Command: {example}")
    print(f"Predicted Main Command: {predicted_main_cmd} (Expected: {true_main_cmd})")
    print(f"Predicted Argument: {predicted_arg} (Expected: {true_arg})")
    print()

    # Check correctness
    if predicted_main_cmd == true_main_cmd:
        correct_main_cmd += 1
    if predicted_arg == true_arg:
        correct_arg += 1

# Calculate accuracy
main_cmd_accuracy = correct_main_cmd / total_examples * 100
arg_accuracy = correct_arg / total_examples * 100

# Display accuracy
print(f"Main Command Prediction Accuracy: {main_cmd_accuracy:.2f}%")
print(f"Argument Prediction Accuracy: {arg_accuracy:.2f}%")


