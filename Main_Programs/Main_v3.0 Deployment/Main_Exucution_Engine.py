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
from rag_command_parser import generate_natural_processing_output
import pyttsx3
from groq import Groq
import re

recognizer = sr.Recognizer()
try:
    tts_engine = pyttsx3.init('sapi5')
    voices = tts_engine.getProperty('voices')
    if voices:
        tts_engine.setProperty('voice', voices[0].id)
    tts_engine.setProperty('rate', 200)
    tts_engine.setProperty('volume', 0.9)
except Exception as e:
    print(f"Warning: Could not initialize TTS engine: {e}")
    tts_engine = None

def speak_text(text):
    if tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    else:
        print(f"TTS: {text}")

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


# Improved parameter normalization for robust command execution
PARAMETER_ALIASES = {
    'click on': ['element_name', 'item', 'text', 'target', 'target_name'],
    'write text': ['text', 'content', 'message'],
    'open website': ['url', 'website', 'link'],
    'open application': ['application', 'app', 'program', 'name'],
    'close application': ['application', 'app', 'program', 'name'],
    'web search': ['query', 'search', 'text'],
    'youtube search': ['query', 'search', 'text'],
    'get weather': ['city_name', 'city', 'location'],
    'open browser': ['browser', 'name'],
    # Add more as needed
}

def normalize_parameters(action, parameters):
    """Map incoming parameters to the expected argument names for the command."""
    if not parameters:
        return {}
    if action in PARAMETER_ALIASES:
        aliases = PARAMETER_ALIASES[action]
        # Try to match any alias
        for expected in aliases:
            for key in parameters:
                if key == expected:
                    return {expected: parameters[key]}
            for key in parameters:
                if key in aliases:
                    return {expected: parameters[key]}
        # If no match, just return the first value with the expected key
        if parameters:
            value = list(parameters.values())[0]
            return {aliases[0]: value}
    # If not in aliases, try to use the first value as positional
    if parameters:
        return {list(parameters.keys())[0]: list(parameters.values())[0]}
    return parameters

# Use a fast, instruction-tuned model for dynamic code generation
from groq import Groq

def execute_direct_code_generation_with_confirmation(user_input):
    api_key = os.getenv('GROQ_API_KEY', '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')
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client for code generation: {e}")
        return False, "Sorry, I couldn't generate code for your command."
    prompt = (
        f"Generate Python code to: {user_input}.\n"
        f"User wants to execute this code to complete the activity on a Windows device.\n"
        f"Code must be oriented and compatible to execute on Windows 11.\n"
        f"Code must be efficient and fast to execute.\n"
        f"Do not add explanations or comments."
    )
    try:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        generated_code = completion.choices[0].message.content
        code_match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)
        if code_match:
            generated_code = code_match.group(1).strip()
        else:
            print("No valid code detected in response!")
            return False, "Sorry, I couldn't generate code for your command."
        print("Generated Code:\n")
        print(generated_code)
        try:
            print("\nExecuting the Generated Code...\n")
            exec(generated_code)
            print("\nTask completed successfully!")
            return True, "Task completed successfully!"
        except Exception as e:
            print(f"\nAn error occurred while executing the generated code: {e}")
            return False, f"An error occurred while executing the generated code: {e}"
    except Exception as e:
        print(f"Error generating code: {e}")
        return False, f"Error generating code: {e}"

# Use a rich, robust model for confirmations and error replies

# --- Model selection ---
NATURAL_REPLY_MODEL = "llama-3.3-70b-versatile"
ERROR_REPLY_MODEL = "llama-3.3-70b-versatile"
DYNAMIC_CODE_MODEL = "gemma2-9b-it"

def generate_natural_reply(user_command, task_plan):
    api_key = os.getenv('GROQ_API_KEY', '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')
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client for reply: {e}")
        return "Task completed."
    prompt = (
        f"You are a helpful AI assistant.\n"
        f"The user gave the following command: '{user_command}'.\n"
        f"Here is the structured plan that was executed: {task_plan}\n"
        f"Summarize in a friendly, natural way what was done, as if speaking to the user.\n"
        f"Be concise, clear, and conversational.\n"
        f"If the task involved multiple steps, mention them briefly.\n"
        f"Do not include code or technical details.\n"
        f"End with a prompt for the next command, like 'What would you like to do next?'\n"
    )
    try:
        completion = client.chat.completions.create(
            model=NATURAL_REPLY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=120,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        reply = completion.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print(f"Error generating natural reply: {e}")
        return "Task completed. What would you like to do next?"


def generate_natural_error_reply(user_command, error):
    api_key = os.getenv('GROQ_API_KEY', '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')
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client for error reply: {e}")
        return f"Sorry, something went wrong while processing your command: {user_command}. Please try again."
    prompt = (
        f"You are a helpful AI assistant.\n"
        f"The user gave the following command: '{user_command}'.\n"
        f"An error occurred: {error}\n"
        f"Generate a friendly, conversational response to let the user know there was a problem, but encourage them to try again or clarify.\n"
        f"Do not include technical details unless helpful.\n"
        f"Only output the sentence, nothing else."
    )
    try:
        completion = client.chat.completions.create(
            model=ERROR_REPLY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=80,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        reply = completion.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print(f"Error generating natural error reply: {e}")
        return f"Sorry, something went wrong while processing your command: {user_command}. Please try again."


def execute_task_plan(task_json, user_command=None):
    try:
        task_plan = json.loads(task_json)
        steps = task_plan.get("steps", [])
        
        # Only provide per-step feedback for multi-step tasks
        multi_step = len(steps) > 1
        for idx, step in enumerate(steps, 1):
            action = step.get("action")
            parameters = step.get("parameters", {})
            if multi_step:
                user_friendly = generate_natural_processing_output(action, step=idx)
                speak_text(user_friendly)
            try:
                if action in commands:
                    # Normalize parameters before calling the command
                    norm_params = normalize_parameters(action, parameters)
                    try:
                        if norm_params:
                            commands[action](**norm_params)
                        else:
                            commands[action]()
                    except TypeError as e:
                        # Try with first value as positional
                        try:
                            if parameters:
                                commands[action](*list(parameters.values()))
                            else:
                                commands[action]()
                        except Exception as e2:
                            # Try with no parameters
                            try:
                                commands[action]()
                            except Exception as e3:
                                # Fallback to dynamic code generation
                                print(f"[ERROR] All attempts failed for command {action}: {e3}")
                                success, dyn_msg = execute_direct_code_generation_with_confirmation(f"{action} {json.dumps(parameters)}")
                                speak_text(dyn_msg)
                                continue
                elif "open application" in action:
                    app_name = parameters.get("application", "") or parameters.get("app", "") or parameters.get("name", "")
                    app_name = app_name.strip()
                    if not app_handler.open_application(app_name):
                        app_handler.open_application_fallback(app_name)
                elif "close application" in action:
                    app_name = parameters.get("application", "") or parameters.get("app", "") or parameters.get("name", "")
                    app_name = app_name.strip()
                    app_handler.close_application(app_name)
                elif "web search" in action:
                    search_query = parameters.get("query", "") or parameters.get("search", "") or parameters.get("text", "")
                    search_query = search_query.strip()
                    if "web search" in commands:
                        commands["web search"](search_query)
                elif "youtube search" in action:
                    youtube_query = parameters.get("query", "") or parameters.get("search", "") or parameters.get("text", "")
                    youtube_query = youtube_query.strip()
                    if "youtube search" in commands:
                        commands["youtube search"](youtube_query)
                elif "open website" in action:
                    website_url = parameters.get("url", "") or parameters.get("website", "") or parameters.get("link", "")
                    website_url = website_url.strip()
                    if hasattr(web_functions, "open_website"):
                        web_functions.open_website(website_url)
                elif "write text" in action:
                    text_to_write = parameters.get("text", "") or parameters.get("content", "") or parameters.get("message", "")
                    text_to_write = text_to_write.strip()
                    ui_handler.write_text(text_to_write)
                else:
                    print(f"[ERROR] Unknown command: {action}. Attempting to generate dynamically...")
                    success, dyn_msg = execute_direct_code_generation_with_confirmation(f"{action} {json.dumps(parameters)}")
                    speak_text(dyn_msg)
                    continue
            except Exception as e:
                print(f"[ERROR] Error executing command {action}: {e}")
                if user_command:
                    reply = generate_natural_error_reply(user_command, str(e))
                    speak_text(reply)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON format: {e}")
        if user_command:
            reply = generate_natural_error_reply(user_command, str(e))
            speak_text(reply)
    except Exception as e:
        print(f"[ERROR] Unexpected error in execute_task_plan: {e}")
        if user_command:
            reply = generate_natural_error_reply(user_command, str(e))
            speak_text(reply)


# --- Improved wake word detection ---
def listen_for_wake_word():
    WAKE_WORDS = ["hey nexa", "ok nexa", "hello nexa", "hey alexa", "ok alexa", "hello alexa"]
    recognizer = sr.Recognizer()
    speak_text("Say 'Hey Nexa' to wake me up.")
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                print("[Wake Word] Listening for wake word...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=4)
                try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"[Wake Word] Heard: {command}")
                    for word in WAKE_WORDS:
                        if word in command:
                            speak_text("I'm listening.")
                            return
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue
            except sr.WaitTimeoutError:
                continue

# --- Retry logic for failed commands ---
def listen_for_command_with_feedback():
    while True:
        command = None
        try:
            command = listen_command_with_timeout(timeout=10)
        except Exception:
            pass
        if command is None or command.strip() == "":
            speak_text("Going to sleep. Say 'Hey Nexa' to wake me up.")
            listen_for_wake_word()
            continue
        return command

# Helper: listen_command with timeout

def listen_command_with_timeout(timeout=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            # Wait up to 3s for speech to start, then allow up to 12s for the full utterance
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=12)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
    return None


if __name__ == "__main__":
    try:
        speak_text("Hello! I'm ready for your command.")
        while True:
            user_input = listen_for_command_with_feedback()
            if user_input.lower() in ['exit', 'quit', 'stop']:
                speak_text("Exiting. Goodbye!")
                print("Exiting...")
                break
            Modified_Input = basic_rag(user_input)
            if Modified_Input:
                task_plan = generate_task_plan(Modified_Input)
                if not task_plan or not task_plan.get("steps"):
                    speak_text("Sorry, I couldn't understand your command. Could you please clarify?")
                    continue
                try:
                    execute_task_plan(json.dumps(task_plan), user_command=user_input)
                    # Only speak the final reply for single-step, or after all steps for multi-step
                    reply = generate_natural_reply(user_input, task_plan)
                    speak_text(reply)
                except Exception as e:
                    print(f"[Main Loop] Error: {e}")
                    speak_text("Something went wrong. Would you like to try again? Please repeat your command.")
                    continue
            else:
                speak_text("Sorry, I couldn't understand your command. Could you please repeat?")
    except KeyboardInterrupt:
        speak_text("Exiting. Goodbye!")
        print("\nExiting...")
    except Exception as e:
        speak_text("An unexpected error occurred. Please try again.")
        print(f"[ERROR] Unexpected error in main loop: {e}")