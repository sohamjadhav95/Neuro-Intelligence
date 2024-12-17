import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize microphone
while True:
    with sr.Microphone() as source:
        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            # Using Google Speech API (no large models to download)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print("You said:", command)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech API; {0}".format(e))
