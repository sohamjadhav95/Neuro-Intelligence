from transformers import BertTokenizer, BertModel
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already done
nltk.download('stopwords')
stop_words = stopwords.words('english')

# Load dataset
data = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random Forest 2\generated_dataset_50000_rows.csv")

# Preprocess text (lowercase, remove stopwords)
def preprocess_text(text):
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

data['command_text'] = data['natural_language_command'].apply(preprocess_text)

# Features and Labels
X = data['command_text']
y_main = data['main_command']  # Main Command labels
y_argument = data['argument']  # Argument labels

# Split data
X_train, X_test, y_train_main, y_test_main = train_test_split(X, y_main, test_size=0.2, random_state=42)
X_train, X_test, y_train_argument, y_test_argument = train_test_split(X, y_argument, test_size=0.2, random_state=42)

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get BERT embeddings
def get_bert_embeddings(texts):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=128)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Convert text data to BERT embeddings
print("Generating BERT embeddings for training data...")
X_train_embeddings = get_bert_embeddings(X_train.tolist())
X_test_embeddings = get_bert_embeddings(X_test.tolist())

# Train Random Forest for Main Command Classification
rf_main = RandomForestClassifier(n_estimators=100, random_state=42)
rf_main.fit(X_train_embeddings, y_train_main)

# Train Random Forest for Argument Classification
rf_argument = RandomForestClassifier(n_estimators=100, random_state=42)
rf_argument.fit(X_train_embeddings, y_train_argument)

# Evaluate Main Command Classifier
y_pred_main = rf_main.predict(X_test_embeddings)
print("Main Command Classification Report:")
print(classification_report(y_test_main, y_pred_main))

# Evaluate Argument Classifier
y_pred_argument = rf_argument.predict(X_test_embeddings)
print("Argument Classification Report:")
print(classification_report(y_test_argument, y_pred_argument))

from sklearn.utils import resample
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

# Apply SMOTE to minority classes
X_train_upsampled, y_train_upsampled = SMOTE.fit_resample(X_train_embeddings, y_train_argument)

# Apply Downsampling to the upsampled dataset
train_data = pd.DataFrame(X_train_upsampled)
train_data['label'] = y_train_upsampled

majority_class = train_data[train_data['label'] == 'majority_class_label']
minority_class = train_data[train_data['label'] == 'minority_class_label']

# Downsample majority class
majority_downsampled = resample(
    majority_class,
    replace=False,
    n_samples=len(minority_class),
    random_state=42
)

# Combine into a balanced dataset
balanced_data = pd.concat([majority_downsampled, minority_class])
X_train_balanced = balanced_data.drop(columns=['label']).values
y_train_balanced = balanced_data['label'].values


# Prediction Function
def predict_command_and_argument(command):
    command = preprocess_text(command)
    command_embedding = get_bert_embeddings([command])
    
    main_pred = rf_main.predict(command_embedding)
    argument_pred = rf_argument.predict(command_embedding)
    
    return main_pred[0], argument_pred[0]

# Example Usage
command = "please open chrome browser"
main_command, argument = predict_command_and_argument(command)
print(f"Main Command: {main_command}, Argument: {argument}")
