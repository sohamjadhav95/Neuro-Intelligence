import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Load Dataset
df = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random Forest 2\generated_dataset_50000_rows.csv")


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


# Example Testing Commands
examples = [
    "open YouTube app",             # Expected: "open_application YouTube"
    "search for global trends",     # Expected: "search global_trends"
    "create a new folder",          # Expected: "create_folder new"
    "play some music",              # Expected: "play music"
    "check the battery status",     # Expected: "check_battery status"
    "shut down the computer",       # Expected: "shutdown computer"
    "find me a recipe for pasta",   # Expected: "search pasta_recipe"
    "show today's weather",         # Expected: "show_weather today"
    "close the browser",            # Expected: "close_application browser"
    "move file to documents",       # Expected: "move_file documents"
]

# Predict and print results
for command in examples:
    predict_main_and_argument(command)


from sklearn.metrics import classification_report

# Predict on Test Set for Main Command
y_main_pred = main_model.predict(X_test_vec)
main_command_report = classification_report(y_main_test, y_main_pred, target_names=le_main_command.classes_)

# Predict on Test Set for Argument
y_arg_pred = arg_model.predict(X_test_vec)
argument_report = classification_report(y_arg_test, y_arg_pred, target_names=le_argument.classes_)

# Display Reports
print("Main Command Classification Report:")
print(main_command_report)

print("\nArgument Classification Report:")
print(argument_report)
