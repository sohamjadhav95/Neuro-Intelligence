from fuzzywuzzy import process
import joblib
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

class SimpleCommandPredictor:
    def __init__(self):
        # Command patterns
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
        
        # Try to load models, but don't fail if they're not available
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
        
        # If no direct match, use fuzzy matching
        all_patterns = []
        for command, patterns in self.command_patterns.items():
            all_patterns.extend([(pattern, command) for pattern in patterns])
        
        best_match = process.extractOne(nl_command, [p[0] for p in all_patterns])
        if best_match[1] > 60:  # If similarity is above 60%
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
        
        # Check for direct matches first
        for arg in relevant_args:
            if arg in nl_command:
                return arg
        
        # If no direct match, use fuzzy matching
        best_match = process.extractOne(nl_command, relevant_args)
        if best_match[1] > 60:  # If similarity is above 60%
            return best_match[0]
        
        return 'unknown_argument'

    def predict(self, nl_command):
        main_command = self.predict_main_command(nl_command)
        argument = self.predict_argument(nl_command, main_command)
        return main_command, argument

def predict_command(nl_command):
    predictor = SimpleCommandPredictor()
    return predictor.predict(nl_command)

if __name__ == "__main__":
    # Comprehensive test cases grouped by command type
    test_commands = [
        # Open Application Commands - Various phrasings
        "open chrome please",
        "launch firefox browser",
        "can you start vscode",
        "run microsoft word",
        "execute matlab program",
        "start up powerpoint presentation",
        "open calculator app",
        "launch photoshop software",
        "start notepad application",
        "open terminal window",
        
        # Close Application Commands
        "close chrome browser",
        "exit microsoft word",
        "quit spotify please",
        "terminate excel application",
        "shut down calculator",
        "close firefox window",
        "exit vscode editor",
        "quit matlab program",
        
        # System Status Commands
        "check battery status",
        "show cpu usage",
        "display memory usage",
        "what's the current disk space",
        "monitor network status",
        "how much battery is left",
        "check system resources",
        "show me the cpu load",
        "display available disk space",
        "what's the memory utilization",
        
        # Web Search Commands
        "search for weather forecast",
        "find nearby restaurants",
        "look up latest news",
        "google some recipes",
        "search for movie showtimes",
        "find available flights",
        "look up job opportunities",
        "search online courses",
        "find product reviews",
        "search for coding tutorials",
        
        # Media Control Commands
        "turn volume up",
        "increase the volume",
        "decrease brightness",
        "adjust screen brightness",
        "mute the sound",
        "unmute audio",
        "set volume to low",
        "make screen brighter",
        "turn down the volume",
        "increase screen brightness",
        
        # Complex/Mixed Commands
        "can you please open chrome and search for restaurants",
        "check cpu usage and display memory status",
        "launch spotify and turn up the volume",
        "open word and close excel",
        "search weather and start calculator",
        
        # Informal/Conversational Commands
        "hey could you open chrome for me",
        "i need to check the cpu usage",
        "would you mind closing excel",
        "can you tell me the battery status",
        "i want to search for some recipes",
        
        # Commands with Extra Words/Noise
        "please kindly open the chrome browser window if you can",
        "i really need you to check the current cpu usage right now",
        "could you possibly search for some good restaurants nearby",
        "just need to quickly launch the calculator app please",
        "would you be able to turn up the volume a little bit",
        
        # Edge Cases
        "open",  # Incomplete command
        "search",  # Missing search term
        "check status",  # Ambiguous system metric
        "launch something",  # Undefined application
        "adjust",  # Incomplete media command
        "chrome",  # Just application name
        "volume",  # Ambiguous media command
        "brightness please",  # Ambiguous direction
        
        # Potential Error Cases
        "",  # Empty command
        "do something",  # Very vague
        "open nonexistent_app",  # Invalid application
        "make coffee",  # Out of scope command
        "play music loudly",  # Ambiguous media command
        "check weather in paris",  # Complex web search
    ]
    
    predictor = SimpleCommandPredictor()
    print("Testing Command Prediction System")
    print("=" * 50)
    
    # Group results by command type for better readability
    results = {
        'open_application': [],
        'close_application': [],
        'system_status': [],
        'web_search': [],
        'media_control': [],
        'unknown_command': []
    }
    
    # Process all test cases
    for cmd in test_commands:
        main_cmd, arg = predictor.predict(cmd)
        results[main_cmd if main_cmd in results else 'unknown_command'].append({
            'input': cmd,
            'main_cmd': main_cmd,
            'arg': arg
        })
    
    # Display results by category
    for category, commands in results.items():
        if commands:
            print(f"\n\n{category.upper().replace('_', ' ')} COMMANDS")
            print("-" * 50)
            for cmd in commands:
                print(f"\nInput: {cmd['input']}")
                print(f"Predicted Main Command: {cmd['main_cmd']}")
                print(f"Predicted Argument: {cmd['arg']}")
    
    # Print statistics
    print("\n\nTEST STATISTICS")
    print("=" * 50)
    total_commands = len(test_commands)
    recognized_commands = sum(1 for cmd in test_commands if predictor.predict(cmd)[0] != 'unknown_command')
    success_rate = (recognized_commands / total_commands) * 100
    
    print(f"Total test commands: {total_commands}")
    print(f"Successfully recognized: {recognized_commands}")
    print(f"Recognition rate: {success_rate:.2f}%")
    
    # Category distribution
    print("\nCommand Distribution:")
    for category, commands in results.items():
        percentage = (len(commands) / total_commands) * 100
        print(f"{category}: {len(commands)} commands ({percentage:.1f}%)")