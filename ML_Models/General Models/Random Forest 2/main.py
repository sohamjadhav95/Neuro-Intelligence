import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Preprocess text (lowercase, optional stopword removal)
def preprocess_text(text, remove_stopwords=False):
    text = text.lower()
    if remove_stopwords:
        text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Load dataset
data = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random Forest 2\generated_dataset_50000_rows.csv")
data.dropna(subset=['natural_language_command', 'main_command', 'argument'], inplace=True)
data['command_text'] = data['natural_language_command'].apply(preprocess_text)

# Features and labels
X = data['command_text']
y_main = data['main_command']
y_argument = data['argument']

# Train-test split
X_train, X_test, y_train_main, y_test_main, y_train_argument, y_test_argument = train_test_split(
    X, y_main, y_argument, test_size=0.2, random_state=42)

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train Main Command Classifier
rf_main = RandomForestClassifier(n_estimators=100, random_state=42)
rf_main.fit(X_train_tfidf, y_train_main)

# Train Argument Classifier
rf_argument = RandomForestClassifier(n_estimators=100, random_state=42)
rf_argument.fit(X_train_tfidf, y_train_argument)

# Evaluate Main Command Classifier
y_pred_main = rf_main.predict(X_test_tfidf)
print("Main Command Classification Report:")
print(classification_report(y_test_main, y_pred_main))

# Evaluate Argument Classifier
y_pred_argument = rf_argument.predict(X_test_tfidf)
print("Argument Classification Report:")
print(classification_report(y_test_argument, y_pred_argument))

# Predict Function
def predict_command_and_argument(command):
    try:
        command = preprocess_text(command)
        command_tfidf = tfidf_vectorizer.transform([command])
        main_pred = rf_main.predict(command_tfidf)
        argument_pred = rf_argument.predict(command_tfidf)
        return main_pred[0], argument_pred[0]
    except Exception as e:
        return f"Error during prediction: {str(e)}"

# Example Usage
command = "please open chrome browser"
main_command, argument = predict_command_and_argument(command)
print(f"Main Command: {main_command}, Argument: {argument}")
