import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pickle
import re

class LightweightCommandExtractor:
    def __init__(self):
        # Initialize pipelines for command and argument extraction
        self.command_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        self.argument_extractors = {}
        
    def preprocess_text(self, text):
        """Basic text preprocessing"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text
    
    def train(self, data_path):
        """Train the model on the provided dataset"""
        # Load data
        df = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random forest Model\natural_language_commands.csv")
        
        # Preprocess text
        X = df['natural_language_command'].apply(self.preprocess_text)
        y_command = df['main_command']
        
        # Train command classifier
        self.command_pipeline.fit(X, y_command)
        
        # Store unique commands for later use
        self.commands = y_command.unique()
        
        # Create argument patterns for each command type
        self.create_argument_patterns(df)
        
        return self
    
    def create_argument_patterns(self, df):
        """Create simple patterns for argument extraction"""
        for command in self.commands:
            command_data = df[df['main_command'] == command]
            arguments = command_data['argument'].unique()
            
            # Create pattern dictionary for each command
            self.argument_extractors[command] = {
                arg: self.create_pattern_for_argument(arg) 
                for arg in arguments
            }
    
    def create_pattern_for_argument(self, argument):
        """Create regex pattern for argument extraction"""
        # Convert argument to regex pattern
        # This is a simplified version - can be made more sophisticated
        words = argument.split()
        pattern = r'.*?(' + '|'.join(words) + r').*?'
        return re.compile(pattern, re.IGNORECASE)
    
    def predict(self, text):
        """Predict command and extract argument from text"""
        # Preprocess input text
        processed_text = self.preprocess_text(text)
        
        # Predict command
        command = self.command_pipeline.predict([processed_text])[0]
        
        # Extract argument based on command type
        argument = self.extract_argument(text, command)
        
        return {
            'command': command,
            'argument': argument
        }
    
    def extract_argument(self, text, command):
        """Extract argument based on command type and patterns"""
        text = text.lower()
        
        # Get patterns for this command type
        patterns = self.argument_extractors.get(command, {})
        
        # Try to match patterns
        for arg, pattern in patterns.items():
            if pattern.search(text):
                return arg
                
        return None
    
    def save_model(self, path):
        """Save the trained model"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(path):
        """Load a trained model"""
        with open(path, 'rb') as f:
            return pickle.load(f)
    
    def evaluate(self, test_data_path):
        """Evaluate the model on the provided test dataset"""
        # Load test data
        df_test = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Random forest Model\natural_language_commands.csv")
        
        # Preprocess text
        X_test = df_test['natural_language_command'].apply(self.preprocess_text)
        y_test = df_test['main_command']
        
        # Predict commands
        y_pred = self.command_pipeline.predict(X_test)
        
        # Calculate accuracy
        accuracy = np.mean(y_pred == y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")
        
    

# Example usage
def main():
    # Create and train model
    extractor = LightweightCommandExtractor()
    extractor.train(r"E:\Projects\VoxSys\Models Creating\Random forest Model\natural_language_commands.csv")
    
    # Evaluate model
    extractor.evaluate(r"E:\Projects\VoxSys\Models Creating\Random forest Model\natural_language_commands.csv")
    
    # Save model
    extractor.save_model('command_extractor.pkl')
    
    # Test some examples
    test_commands = [
        "please close firefox for me",
        "can you open chrome browser",
        "search for restaurants nearby",
        "search for general ai",
        "search what is this"
    ]
    
    for cmd in test_commands:
        result = extractor.predict(cmd)
        print(f"\nInput: {cmd}")
        print(f"Predicted Command: {result['command']}")
        print(f"Extracted Argument: {result['argument']}")

if __name__ == "__main__":
    main()