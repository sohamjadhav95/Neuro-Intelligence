import sys
import os

# Get the current directory and add relative paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "Core_Processes"))
sys.path.append(os.path.join(current_dir, "Dynaminc_Commands_Exucution"))
sys.path.append(os.path.join(current_dir, "Retrival_Agumented_Generation"))

import json
import speech_recognition as sr
from Core_Commands import *
from task_planning import *
from Function_Generation import *
from rag_command_parser import basic_rag

recognizer = sr.Recognizer()

# Function to listen for commands
def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")  
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Noise reduction
        print("Listening...")

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
    
    return None  # Return None if no valid command was detected


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
                except TypeError as e:
                    print(f"[ERROR] Invalid arguments for command: {action} - {e}")
                except Exception as e:
                    print(f"[ERROR] Error executing command {action}: {e}")
          
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
                try:
                    execute_direct_code_generation(action)
                except Exception as e:
                    print(f"[ERROR] Failed to execute dynamic code generation: {e}")
    
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error in execute_task_plan: {e}")


if __name__ == "__main__":
    try:
        while True:
            user_input = input("Enter Input: ")
            if user_input.lower() in ['exit', 'quit', 'stop']:
                print("Exiting...")
                break
                
            Modified_Input = basic_rag(user_input)
            if Modified_Input:
                task_plan = generate_task_plan(Modified_Input)
                execute_task_plan(json.dumps(task_plan))
            else:
                print("No valid command received. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"[ERROR] Unexpected error in main loop: {e}")