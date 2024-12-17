import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import joblib

def preprocess_dataset(input_file, output_vectorizer):
    # Load dataset
    data = pd.read_csv(input_file)
    
    # Drop rows with missing values
    data = data.dropna(subset=['natural_language_command', 'main_command', 'argument'])
    
    # Split data
    X = data['natural_language_command']
    y_main = data['main_command']
    y_arg = data['argument']
    X_train, X_test, y_main_train, y_main_test, y_arg_train, y_arg_test = train_test_split(
        X, y_main, y_arg, test_size=0.2, random_state=42
    )
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Save vectorizer
    joblib.dump(vectorizer, output_vectorizer)
    return X_train_tfidf, X_test_tfidf, y_main_train, y_main_test, y_arg_train, y_arg_test

if __name__ == "__main__":
    input_file = r"E:\Projects\VoxSys\Models Creating\Random Forest 2\generated_dataset_50000_rows.csv"  # or use the forward slash version

    output_vectorizer = 'tfidf_vectorizer.pkl'
    preprocess_dataset(input_file, output_vectorizer)
    print("Preprocessing complete!")
