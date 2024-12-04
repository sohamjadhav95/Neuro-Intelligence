# The code uses the 'speech_recognition' library to convert speech to text.
# The code uses the 'pyttsx3' library to convert text to speech.

import speech_recognition as sr
import pyttsx3
import time

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Set properties for TTS engine (optional)
tts_engine.setProperty('rate', 100)  # Speed of speech
tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Function to speak text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    time.sleep(1)  # Short delay after speaking
    
# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)

        try:
            # Recognize and print command
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            speak_text(f"You said: {command}")
            return command.lower()

        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak_text("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("Network error.")
            speak_text("Network error.")
            return None

# Example loop to keep listening for commands
while True:
    command = listen_command()
    if command:
        # Simple quit command to stop the loop
        if "exit" in command:
            speak_text("Exiting. Goodbye!")
            break
        
        # Placeholder for handling different commands
        elif "open browser" in command:
            speak_text("Opening browser...")  
            # Insert code here to open browser or other actions
        else:
            speak_text("Command not recognized.")

