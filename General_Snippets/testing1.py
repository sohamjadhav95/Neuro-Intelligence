from vosk import Model, KaldiRecognizer
import pyaudio
import json

def listen_and_transcribe_vosk():
    model = Model("model")  # Replace "model" with the path to your Vosk model
    recognizer = KaldiRecognizer(model, 16000)

    # Setup microphone
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()

    print("Listening... Speak clearly.")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("You said:", result.get("text", ""))
            return result.get("text", "")

# Call the function
listen_and_transcribe_vosk()
