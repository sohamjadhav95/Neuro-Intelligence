import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from preprocess import preprocess_dataset

def train_models():
    # Load preprocessed data
    X_train_tfidf, X_test_tfidf, y_main_train, y_main_test, y_arg_train, y_arg_test = preprocess_dataset(
        r"E:\Projects\VoxSys\Models Creating\Random Forest 2\generated_dataset_50000_rows.csv", 'tfidf_vectorizer.pkl'
    )
    
    # Train Main Command model
    rf_main = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_main.fit(X_train_tfidf, y_main_train)
    y_main_pred = rf_main.predict(X_test_tfidf)
    print("Main Command Classification Report:")
    print(classification_report(y_main_test, y_main_pred))
    joblib.dump(rf_main, 'rf_main_command.pkl')
    
    # Train Argument model
    rf_arg = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_arg.fit(X_train_tfidf, y_arg_train)
    y_arg_pred = rf_arg.predict(X_test_tfidf)
    print("Argument Extraction Classification Report:")
    print(classification_report(y_arg_test, y_arg_pred))
    joblib.dump(rf_arg, 'rf_argument_extraction.pkl')

if __name__ == "__main__":
    train_models()
    print("Training complete!")
