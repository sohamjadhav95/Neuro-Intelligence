import speech_recognition as sr
import pyautogui
import pyttsx3
import numpy as np
import time
import threading
import cv2
import pytesseract
from PIL import ImageGrab

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Function to Convert Text to Speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Grid Size (Adjust as needed)
GRID_SIZE = 9  # 3x3 grid
grid_cells = []
selected_cell = None

# Function to Create Grid and Visualize (Optional)
def create_grid():
    global grid_cells
    screen_width, screen_height = pyautogui.size()
    cell_width = screen_width // int(np.sqrt(GRID_SIZE))
    cell_height = screen_height // int(np.sqrt(GRID_SIZE))
    
    grid_cells = []  # Clear grid_cells before adding new ones
    for i in range(int(np.sqrt(GRID_SIZE))):
        for j in range(int(np.sqrt(GRID_SIZE))):
            x = j * cell_width
            y = i * cell_height
            grid_cells.append((x, y, cell_width, cell_height))
    speak(f"Created a grid with {GRID_SIZE} cells.")

# Function to Handle Mouse Movement to Selected Cell
def move_mouse_to_selected_cell(cell_index):
    global selected_cell
    if cell_index < len(grid_cells):
        x, y, _, _ = grid_cells[cell_index]
        pyautogui.moveTo(x + 10, y + 10)  # Adjust the offset as needed
        selected_cell = cell_index
        speak(f"Moved to cell {cell_index+1}")
    else:
        speak("Invalid cell selection")

# Function to Highlight On-Screen Text for Similar Choices
def highlight_on_screen_text(similar_choices):
    # Use OCR to extract text from the screen
    screen_text = pytesseract.image_to_string(ImageGrab.grab())
    
    # Find similar choices in the screen text
    for choice in similar_choices:
        if choice in screen_text:
            # Highlight the choice on the screen (simplified example, may require more sophisticated approach)
            print(f"Highlighting: {choice}")
            # Implement actual highlighting (e.g., using OpenCV to draw rectangles around the text)

# Function to Handle Voice Commands
def handle_command(command):
    global selected_cell
    command = command.lower()
    print(f"Recognized Command: {command}")
    speak(f"Executing command: {command}")
    
    if "create grid" in command:
        create_grid()
        
    elif "select cell" in command:
        try:
            cell_number = int(''.join(filter(str.isdigit, command)))
            move_mouse_to_selected_cell(cell_number - 1)  # Adjust for 0-based index
        except ValueError:
            speak("Please specify a valid cell number")
            
    elif "move up" in command and selected_cell is not None:
        new_cell_index = selected_cell - int(np.sqrt(GRID_SIZE))
        if new_cell_index >= 0:
            move_mouse_to_selected_cell(new_cell_index)
        else:
            speak("Already at top row")
            
    elif "move down" in command and selected_cell is not None:
        new_cell_index = selected_cell + int(np.sqrt(GRID_SIZE))
        if new_cell_index < len(grid_cells):
            move_mouse_to_selected_cell(new_cell_index)
        else:
            speak("Already at bottom row")
            
    elif "move left" in command and selected_cell is not None:
        new_cell_index = selected_cell - 1
        if new_cell_index >= 0 and new_cell_index // int(np.sqrt(GRID_SIZE)) == selected_cell // int(np.sqrt(GRID_SIZE)):
            move_mouse_to_selected_cell(new_cell_index)
        else:
            speak("Already at leftmost column")
            
    elif "move right" in command and selected_cell is not None:
        new_cell_index = selected_cell + 1
        if new_cell_index < len(grid_cells) and new_cell_index // int(np.sqrt(GRID_SIZE)) == selected_cell // int(np.sqrt(GRID_SIZE)):
            move_mouse_to_selected_cell(new_cell_index)
        else:
            speak("Already at rightmost column")
            
    elif "click" in command and selected_cell is not None:
        pyautogui.click()
        speak("Clicked")
        
    elif "double click" in command and selected_cell is not None:
        pyautogui.doubleClick()
        speak("Double clicked")
        
    elif "show choices" in command:
        similar_choices = ["choice a", "choice b", "choice c"]
        highlight_on_screen_text(similar_choices)

# Example of continuous listening for commands
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for commands...")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                handle_command(command)
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Please repeat.")
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                break

# Start listening in a separate thread
thread = threading.Thread(target=listen_for_commands)
thread.start()
