import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load Dataset
df = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random forest Model\natural_language_commands.csv")


# Preprocess
df['natural_language_command'] = df['natural_language_command'].str.lower()

# Encode Target Labels
le_argument = LabelEncoder()
df['argument_label'] = le_argument.fit_transform(df['argument'])

le_command = LabelEncoder()
df['main_command_label'] = le_command.fit_transform(df['main_command'])

# Split Data
X = df['natural_language_command']
y_argument = df['argument_label']
y_main_command = df['main_command_label']

X_train, X_test, y_arg_train, y_arg_test = train_test_split(X, y_argument, test_size=0.15, random_state=42)
_, _, y_cmd_train, y_cmd_test = train_test_split(X, y_main_command, test_size=0.15, random_state=42)

# Vectorize Text
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Argument Model
arg_model = SVC(kernel='linear')
arg_model.fit(X_train_vec, y_arg_train)

# Train Main Command Model
cmd_model = SVC(kernel='linear')
cmd_model.fit(X_train_vec, y_cmd_train)

# Evaluate
y_arg_pred = arg_model.predict(X_test_vec)
y_cmd_pred = cmd_model.predict(X_test_vec)

print("Argument Prediction Metrics:")
print(classification_report(y_arg_test, y_arg_pred, target_names=le_argument.classes_))

print("Main Command Prediction Metrics:")
print(classification_report(y_cmd_test, y_cmd_pred, target_names=le_command.classes_))


# Real Test Examples
real_examples = [
    "can you show me battery status",    # Expected: battery
    "help me check memory usage",        # Expected: memory usage
    "please open calculator",            # Expected: calculator
    "find tutorials for programming",    # Expected: tutorials
    "terminate firefox now",             # Expected: firefox
]

# Preprocess Real Examples
real_examples_processed = [cmd.lower() for cmd in real_examples]

# Transform Examples to TF-IDF
real_examples_vec = vectorizer.transform(real_examples_processed)

# Predict Arguments
real_predictions = arg_model.predict(real_examples_vec)

# Decode Predictions
decoded_real_predictions = le_argument.inverse_transform(real_predictions)

# Print Results
for command, prediction in zip(real_examples, decoded_real_predictions):
    print(f"Command: {command}")
    print(f"Predicted Argument: {prediction}")
    print()
