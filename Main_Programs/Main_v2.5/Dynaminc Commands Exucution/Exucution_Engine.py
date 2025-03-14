import json
import sys
from task_planning import *
from Function_Generation import *

sys.path.append(r"E:\Projects\Neuro-Intelligence\Main_Programs\Main_v2.5")
from Core_Commands import *


'''
# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            # Using Google Speech API (no large models to download)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech API; {0}".format(e))
'''

def execute_task_plan(task_json):
    try:
        task_plan = json.loads(task_json)
        steps = task_plan.get("steps", [])
        
        for step in steps:
            action = step.get("action")
            parameters = step.get("parameters", {})
            
            if action in commands:
                try:
                    if parameters:
                        commands[action](**parameters)
                    else:
                        commands[action]()
                except TypeError:
                    print(f"[ERROR] Invalid arguments for command: {action}")
          
            elif "open application" in action:
                app_name = parameters.get("application", "").strip()
                if not app_handler.open_application(app_name):
                    app_handler.open_application_fallback(app_name)
            
            elif "close application" in action:
                app_name = parameters.get("application", "").strip()
                app_handler.close_application(app_name)
            
            elif "web search" in action:
                search_query = parameters.get("query", "").strip()
                if "web search" in commands:
                    commands["web search"](search_query)
            
            elif "youtube search" in action:
                youtube_query = parameters.get("query", "").strip()
                if "youtube search" in commands:
                    commands["youtube search"](youtube_query)
            
            elif "open website" in action:
                website_url = parameters.get("url", "").strip()
                if hasattr(web_functions, "open_website"):
                    web_functions.open_website(website_url)
            
            elif "write text" in action:
                text_to_write = parameters.get("text", "").strip()
                print(f"Text to write: {text_to_write}")  # Debugging line
                ui_handler.write_text(text_to_write)

            else:
                print(f"[ERROR] Unknown command: {action}. Attempting to generate dynamically...")
                execute_direct_code_generation(user_input)
    
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")


if __name__ == "__main__":
    user_input = input("Enter command: ")
    task_plan = generate_task_plan(user_input)
    execute_task_plan(json.dumps(task_plan))