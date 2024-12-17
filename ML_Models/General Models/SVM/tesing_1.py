# Evaluate Model
from sklearn.metrics import accuracy_score
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

    return main_command, argument


# Predict on Test Data
y_main_pred = main_model.predict(X_test_vec)
y_arg_pred = arg_model.predict(X_test_vec)

# Calculate Accuracy
main_command_accuracy = accuracy_score(y_main_test, y_main_pred) * 100
argument_accuracy = accuracy_score(y_arg_test, y_arg_pred) * 100

print(f"Main Command Prediction Accuracy: {main_command_accuracy:.2f}%")
print(f"Argument Prediction Accuracy: {argument_accuracy:.2f}%")

# Classification Reports
print("\nClassification Report for Main Command:")
print(classification_report(y_main_test, y_main_pred, target_names=le_main_command.classes_))

print("\nClassification Report for Argument:")
print(classification_report(y_arg_test, y_arg_pred, target_names=le_argument.classes_))

# Real Examples for Testing
real_examples = [
    "can you show me battery status",
    "help me check memory usage",
    "please open calculator",
    "terminate firefox now",
    "launch spotify, please",
    "check the CPU usage",
    "search for Python tutorials online",
    "tell me about the internet connection",
    "close PowerPoint now",
    "turn the volume up"
]

print("\nTesting with Real Examples:")
for example in real_examples:
    predicted_main_cmd, predicted_arg = predict_main_and_argument(example)
    print(f"Input: {example}")
    print(f"Predicted Main Command: {predicted_main_cmd}")
    print(f"Predicted Argument: {predicted_arg}")
    print("-" * 50)
