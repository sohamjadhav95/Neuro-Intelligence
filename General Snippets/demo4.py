import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_and_evaluate_model(csv_file, test_size=0.2, random_state=42):
    """
    Train the SVM model and evaluate its accuracy on the test set.
    :param csv_file: Path to the dataset CSV file.
    :param test_size: Fraction of the dataset to use for testing.
    :param random_state: Seed for reproducibility.
    """
    # Load the dataset
    data = pd.read_csv(csv_file)
    data = data.dropna()  # Remove missing values
    data['User Command'] = data['User Command'].str.lower()  # Normalize input text

    # Split the data into training and testing sets
    X = data['User Command']
    y = data['Exact Command']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Vectorize the text data using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train the SVM model
    svm_model = SVC(kernel='linear', random_state=random_state)
    svm_model.fit(X_train_tfidf, y_train)

    # Make predictions on the test set
    y_pred = svm_model.predict(X_test_tfidf)

    # Calculate and return the accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy:.2%}")

# Define the path to your dataset
dataset_path = "E:\Projects\VoxSys\Main Programs\command_mapping.csv"

# Run the training and evaluation
train_and_evaluate_model(csv_file=dataset_path, test_size=0.2, random_state=42)
