import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import re

def load_command_mapping(csv_file):
    """
    Load command mapping from a CSV file into a dictionary.
    """
    command_mapping = {}
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['User Command'].startswith('#'):  # Skip comment lines
                continue
            trigger = row['User Command'].strip().lower()  # Normalize keywords to lowercase
            command = row['Exact Command'].strip()
            command_mapping[trigger] = command
    return command_mapping

def train_command_model(csv_file):
    """
    Train the SVM model for command identification.
    """
    data = pd.read_csv(csv_file)
    data = data.dropna()
    data['User Command'] = data['User Command'].str.lower()  # Normalize keywords

    # Split data into features (X) and labels (y)
    X = data['User Command']
    y = data['Exact Command']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Vectorize the text data using TF-IDF
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train the SVM model
    svm_model = SVC(kernel='linear', random_state=42)
    svm_model.fit(X_train_tfidf, y_train)
    


def extract_argument(user_input):
    """
    Extract the argument based on the user input and command.
    This can be done using regular expressions or keyword matching.
    """
    user_input = user_input.lower().strip()

    # Extract the app name or argument after the main command
    match = re.search(r"(launch|open|start|run|access|initiate|begin|load|execute|boot|can you open|please launch|help me open|start this program|could you run this app|i need to start this program)\s+(.+)$", user_input)
    
    if match:
        # Extract the argument (the application name)
        return match.group(2).strip()
    
    return None  # If no argument is found

# Main Execution

# Load the command mapping CSV
csv_file = r"E:\Projects\VoxSys\Main Programs\command_mapping_2_columns.csv"
command_mapping = load_command_mapping(csv_file)

# Train the Command Identification Model (Model 1)
svm_model, vectorizer = train_command_model(csv_file)

def execute_command(user_input, svm_model, vectorizer):
    """
    Predict and return the command along with any argument.
    This skips mapping to the dataset and directly outputs the result for processing.
    """
    # Normalize user input
    user_input = user_input.lower().strip()

    # Predict the main command (Model 1)
    user_input_tfidf = vectorizer.transform([user_input])
    predicted_command = svm_model.predict(user_input_tfidf)[0].strip().lower()

    print(f"Predicted Command: {predicted_command}")

    # Extract the argument (Model 2)
    argument = extract_argument(user_input)

    # Avoid redundant appending of arguments
    if argument and argument not in predicted_command:
        full_command = f"{predicted_command} {argument}"
        return full_command
    else:
        return predicted_command
    

