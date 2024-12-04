import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Load the dataset
data_path = r"E:\Projects\VoxSys\Main Programs\command_mapping.csv"
data = pd.read_csv(data_path)

# Step 2: Inspect the dataset
print("Dataset Preview:")
print(data.head())

# Step 3: Data Cleaning
# Assuming columns are 'keyword' (input) and 'command' (output)
data = data.dropna()  # Remove rows with missing values
data['keyword'] = data['keyword'].str.lower()  # Convert to lowercase for uniformity

# Step 4: Split dataset into training and testing
X = data['keyword']
y = data['command']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Step 6: Train an SVM classifier
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train_tfidf, y_train)

# Step 7: Make predictions
y_pred = svm_model.predict(X_test_tfidf)

# Step 8: Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Step 9: Test with new input
def predict_command(input_text):
    input_tfidf = vectorizer.transform([input_text.lower()])
    prediction = svm_model.predict(input_tfidf)
    return prediction[0]

# Example
test_input = "search the web what is living thing"
print(f"Input: '{test_input}' => Predicted Command: '{predict_command(test_input)}'")


