from sklearn.metrics import accuracy_score
import joblib
import warnings
from fuzzywuzzy import process

warnings.filterwarnings('ignore', category=UserWarning)

# Test dataset (you can expand it based on your needs)
test_commands = [
    # Open Application Commands
    ("open chrome please", 'open_application', 'chrome'),
    ("launch firefox browser", 'open_application', 'firefox'),
    ("can you start vscode", 'open_application', 'vscode'),
    # Add more test cases...

    # Close Application Commands
    ("close chrome browser", 'close_application', 'chrome'),
    ("exit microsoft word", 'close_application', 'word'),
    ("quit spotify please", 'close_application', 'spotify'),
    # Add more test cases...

    # System Status Commands
    ("check battery status", 'system_status', 'battery'),
    ("show cpu usage", 'system_status', 'cpu usage'),
    # Add more test cases...
]

class SimpleCommandPredictor:
    def __init__(self):
        self.command_patterns = {
            'open_application': ['open', 'launch', 'start', 'run', 'execute'],
            'close_application': ['close', 'exit', 'quit', 'terminate', 'shut down'],
            'system_status': ['check', 'show', 'display', 'get', 'monitor'],
            'web_search': ['search', 'find', 'look up', 'google', 'browse'],
            'media_control': ['adjust', 'change', 'set', 'modify', 'control']
        }
        
        # Arguments by category
        self.argument_categories = {
            'applications': ['chrome', 'firefox', 'vscode', 'word', 'excel', 'powerpoint', 
                           'spotify', 'notepad', 'calculator', 'terminal', 'matlab', 'photoshop'],
            'system_metrics': ['battery', 'cpu usage', 'memory usage', 'disk space', 'network status'],
            'web_topics': ['weather forecast', 'news', 'recipes', 'movies', 'restaurants', 
                          'hotels', 'flights', 'jobs', 'courses', 'tutorials', 'products', 'reviews'],
            'media_controls': ['volume up', 'volume down', 'brightness up', 'brightness down', 
                             'mute', 'unmute']
        }
        
        # Try to load models
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.rf_main = joblib.load('rf_main_command.pkl')
                self.rf_arg = joblib.load('rf_argument_extraction.pkl')
                self.vectorizer = joblib.load('tfidf_vectorizer.pkl')
        except:
            self.rf_main = self.rf_arg = self.vectorizer = None
    
    def predict_main_command(self, nl_command):
        nl_command = nl_command.lower()
        
        # Try ML model prediction first if available
        try:
            if all([self.rf_main, self.vectorizer]):
                X_tfidf = self.vectorizer.transform([nl_command])
                model_prediction = self.rf_main.predict(X_tfidf)[0]
                if model_prediction in self.command_patterns:
                    return model_prediction
        except:
            pass
        
        # Check for direct pattern matches
        for command, patterns in self.command_patterns.items():
            for pattern in patterns:
                if pattern in nl_command:
                    return command
        
        # Fuzzy matching
        all_patterns = []
        for command, patterns in self.command_patterns.items():
            all_patterns.extend([(pattern, command) for pattern in patterns])
        
        best_match = process.extractOne(nl_command, [p[0] for p in all_patterns])
        if best_match[1] > 60:  # If similarity > 60%
            pattern_index = [p[0] for p in all_patterns].index(best_match[0])
            return all_patterns[pattern_index][1]
        
        return 'unknown_command'
    
    def predict_argument(self, nl_command, main_command):
        nl_command = nl_command.lower()
        
        # Try ML model prediction first if available
        try:
            if all([self.rf_arg, self.vectorizer]):
                X_tfidf = self.vectorizer.transform([nl_command])
                model_prediction = self.rf_arg.predict(X_tfidf)[0]
                # Verify if prediction is in our valid arguments
                for category in self.argument_categories.values():
                    if model_prediction in category:
                        return model_prediction
        except:
            pass
        
        # Select relevant arguments based on main command
        if main_command == 'open_application' or main_command == 'close_application':
            relevant_args = self.argument_categories['applications']
        elif main_command == 'system_status':
            relevant_args = self.argument_categories['system_metrics']
        elif main_command == 'web_search':
            relevant_args = self.argument_categories['web_topics']
        elif main_command == 'media_control':
            relevant_args = self.argument_categories['media_controls']
        else:
            relevant_args = []
            for category in self.argument_categories.values():
                relevant_args.extend(category)
        
        # Check for direct matches
        for arg in relevant_args:
            if arg in nl_command:
                return arg
        
        # Fuzzy matching
        best_match = process.extractOne(nl_command, relevant_args)
        if best_match[1] > 60:  # If similarity > 60%
            return best_match[0]
        
        return 'unknown_argument'

    def predict(self, nl_command):
        main_command = self.predict_main_command(nl_command)
        argument = self.predict_argument(nl_command, main_command)
        return main_command, argument


def test_accuracy():
    predictor = SimpleCommandPredictor()
    
    main_cmd_preds = []
    main_cmd_true = []
    arg_preds = []
    arg_true = []
    
    # Test the model with each command in the dataset
    for command, true_main, true_arg in test_commands:
        pred_main, pred_arg = predictor.predict(command)
        main_cmd_preds.append(pred_main)
        main_cmd_true.append(true_main)
        arg_preds.append(pred_arg)
        arg_true.append(true_arg)
    
    # Calculate accuracy for main command
    main_cmd_accuracy = accuracy_score(main_cmd_true, main_cmd_preds)
    print(f"Main Command Accuracy: {main_cmd_accuracy * 100:.2f}%")
    
    # Calculate accuracy for argument prediction
    arg_accuracy = accuracy_score(arg_true, arg_preds)
    print(f"Argument Accuracy: {arg_accuracy * 100:.2f}%")


if __name__ == "__main__":
    test_accuracy()
