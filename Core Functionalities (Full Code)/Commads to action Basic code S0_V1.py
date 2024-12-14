import speech_recognition as sr
import os
import subprocess

# Initialize the recognizer
r = sr.Recognizer()

# Function to capture audio and convert it to text
def recognize_speech():
    with sr.Microphone() as source:
        print("Please say something...")
        audio = r.listen(source)
        
        try:
            print("Recognizing...")
            # Convert speech to text
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

# Function to execute commands based on recognized text
def execute_command(command):
    if "open browser" in command:
        os.system("start chrome")  # Opens Chrome browser (Windows-specific)
    elif "open notepad" in command:
        os.system("notepad")
    elif "create folder" in command:
        os.makedirs("NewFolder", exist_ok=True)
        print("Folder created")
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")  # Shuts down the computer (Windows-specific)
    else:
        print("Command not recognized.")

# Main function
recognized_text = recognize_speech()
if recognized_text:
    execute_command(recognized_text)
