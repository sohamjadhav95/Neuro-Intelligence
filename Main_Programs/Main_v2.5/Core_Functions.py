import os
import subprocess
import webbrowser
import pyttsx3
import time
import psutil
import shutil
import pywinauto
import requests
import pyautogui
import pytesseract

import speech_recognition as sr
import pygetwindow as gw

from PIL import ImageGrab

from pywinauto.application import Application
from pywinauto import findwindows
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from app_paths import applications_paths, add_custom_app


# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init('sapi5')

# Set properties for TTS engine (optional)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voices', voices[0].id) # Voice for chat
tts_engine.setProperty('rate', 200)  # Speed of speech
tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Function to speak text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    time.sleep(1)  # Short delay after speaking
#-----------------------------------------------------------------------------------------------

# Function to listen for commands
def listen_command():
    with sr.Microphone() as source:
        print("Please speak now...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source, 10, 7)

        try:
            # Using Google Speech API (no large models to download)
            command = recognizer.recognize_google(audio, language= 'en-in')
            print("You said:", command)
            speak_text(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech API; {0}".format(e))
  
        
# Try to open via Start Menu
def search_windows_search_bar(query):
    # Press the Windows key to open the search bar
    pyautogui.hotkey("winleft")
    time.sleep(0.5)  # Wait for the search bar to open

    # Type the query
    pyautogui.write(query, interval=0.1)


# *Application Handling*

class ApplicationHandler:
    
    def __init__(self):
        pass

    def open_application(self, app_name):
        """
        Attempts to open an application by checking a predefined dictionary and the system PATH.
        If unsuccessful, returns False to indicate further methods should be attempted.
        """
        app_command = applications_paths.get(app_name)
        if not app_command:
            add_custom_app(app_name)
            app_command = applications_paths.get(app_name)

        if app_command:
            try:
                speak_text(f"Opening {app_name}...")
                subprocess.Popen([app_command])
                speak_text(f"{app_name} opened.")
                return True
            except FileNotFoundError:
                speak_text(f"Error: Could not open {app_name}. Trying another method...")
                return False

        app_path = shutil.which(app_name.lower())
        if app_path:
            try:
                speak_text(f"Opening {app_name}...")
                subprocess.Popen([app_path])
                return True
            except FileNotFoundError:
                speak_text(f"Error: Could not open {app_name}.")
                return False

        return False

    def open_application_fallback(self, app_name):
        
        """
        Attempts to open an application using Windows Start Menu search as a fallback.
        """
        speak_text(f"Application not available in path, searching for {app_name} in Start Menu...")
        pyautogui.hotkey("winleft")
        pyautogui.write(app_name, interval=0.3)
        
        pyautogui.press("enter")

        
    def close_application(self, app_name):
        """
        Attempts to close an application using window title search or other methods.
        """
        try:
            # Attempt to close using pygetwindow
            windows = gw.getAllTitles()
            matching_windows = [window for window in windows if app_name.lower() in window.lower()]
            if matching_windows:
                for title in matching_windows:
                    win = gw.getWindowsWithTitle(title)[0]
                    win.close()
                speak_text(f"Closing {app_name} using Window...")
                return True
            else:
                speak_text(f"No open window found for {app_name}.")
        except Exception as e:
            speak_text(f"Error closing {app_name} with pygetwindow: {e}")

        try:
            # Attempt to close using pywinauto
            app = Application().connect(title_re=f".*{app_name}.*", timeout=5)
            app.kill()
            speak_text(f"Closing {app_name} using pywinauto...")
            return True
        except Exception as e:
            speak_text(f"Error closing {app_name} with pywinauto: {e}")

        try:
            # Attempt to close using psutil
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    speak_text(f"Closing {app_name} using psutil...")
                    return True
            speak_text(f"Process {app_name} not found.")
        except Exception as e:
            speak_text(f"Error using psutil to close {app_name}: {e}")

        try:
            # Forcefully close using taskkill
            subprocess.run(f"taskkill /f /im {app_name}.exe", check=True, shell=True)
            speak_text(f"Forcefully closing {app_name} using taskkill...")
            return True
        except subprocess.CalledProcessError:
            speak_text(f"Error: Could not close {app_name} using taskkill.")
            return False

app_handler = ApplicationHandler()


# *System Control Functions*
class System_control:

# Increase Volume
    def increase_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(current_volume + 0.1, 1.0)  # Increase by 10%, max is 1
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak_text(f"Volume increased to {int(new_volume * 100)}%.")

    # Decrease Volume
    def decrease_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(current_volume - 0.1, 0.0)  # Decrease by 10%, min is 0
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak_text(f"Volume decreased to {int(new_volume * 100)}%.")

    # Mute Sound
    def mute_sound(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(True, None)
        speak_text("Sound muted.")

    # Unmute Sound
    def unmute_sound(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(False, None)
        speak_text("Sound unmuted.")

    # Sleep Mode
    def sleep_mode(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        speak_text("System is going to sleep mode.")

    # Shutdown with confirmation
    def shutdown(self):
        speak_text("Are you sure you want to shut down the system? Say 'yes' to proceed or 'no' to cancel.")
        confirmation = listen_command()  # Listen for the user's confirmation

        if confirmation is not None:
            if "yes" in confirmation:
                speak_text("Shutting down the system.")
                os.system("shutdown /s /t 1")  # Shutdown immediately
            elif "no" in confirmation:
                speak_text("Shutdown cancelled.")
            else:
                speak_text("Sorry, I didn't catch that. Please say 'yes' or 'no'.")

    # Restart with confirmation
    def restart(self):
        speak_text("Are you sure you want to restart the system? Say 'yes' to proceed or 'no' to cancel.")
        confirmation = listen_command()  # Listen for the user's confirmation

        if confirmation is not None:
            if "yes" in confirmation:
                speak_text("Restarting the system.")
                os.system("shutdown /r /t 1")  # Restart immediately
            elif "no" in confirmation:
                speak_text("Restart cancelled.")
            else:
                speak_text("Sorry, I didn't catch that. Please say 'yes' or 'no'.")
        
system_control = System_control()   
    
# *System Infromation Functions*
class SystemInfromation:
# Battery Status
    def get_battery_status(self):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plug_status = "plugged in" if battery.power_plugged else "not plugged in"
            speak_text(f"Battery is at {percent}% and is {plug_status}.")
        else:
            speak_text("Unable to fetch battery status.")

    # CPU Usage
    def get_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=1)  # Interval gives a more accurate reading
        speak_text(f"Current CPU usage is {cpu_percent}%.")
        
    # Internet Status
    def check_internet(self):
        try:
            subprocess.run(["ping", "8.8.8.8", "-n", "1"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            speak_text("Internet is connected.")
        except subprocess.CalledProcessError:
            speak_text("No internet connection detected.")

    # Current Time
    def get_current_time(self):
        speak_text(f"The current time is {time.strftime('%I:%M %p')}.")

systemInfromation = SystemInfromation()

# *File Operations*

class FileHandler:
    def __init__(self):
        pass

    def create_folder(self, folder_name):
        try:
            os.makedirs(folder_name)
            speak_text(f"Folder '{folder_name}' created successfully.")
        except FileExistsError:
            speak_text(f"Folder '{folder_name}' already exists.")
        except Exception as e:
            speak_text(f"An error occurred: {e}")

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            speak_text(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            speak_text(f"File '{file_path}' not found.")
        except Exception as e:
            speak_text(f"An error occurred: {e}")

    def move_file(self, file_path, destination_folder):
        try:
            shutil.move(file_path, destination_folder)
            speak_text(f"Moved '{file_path}' to '{destination_folder}'.")
        except FileNotFoundError:
            speak_text(f"File '{file_path}' or destination '{destination_folder}' not found.")
        except Exception as e:
            speak_text(f"An error occurred: {e}")

    def rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            speak_text(f"Renamed '{old_name}' to '{new_name}'.")
        except FileNotFoundError:
            speak_text(f"File '{old_name}' not found.")
        except Exception as e:
            speak_text(f"An error occurred: {e}")


file_handler = FileHandler()  # Instantiate FileHandler


# *Web Operations*

class WebFunctions:
    def __init__(self):
        pass  # You can initialize any properties if needed

    # Web Search
    def web_search(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak_text(f"Searching the web for {query}...")

    # YouTube Search
    def youtube_search(self, query):
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        speak_text(f"Searching YouTube for {query}...")

    # Open Website
    def open_website(self, website_url_short):
        # Ensure the URL starts with 'http://' or 'https://'
        if not website_url_short.startswith("http://") and not website_url_short.startswith("https://"):
            website_url = "http://" + website_url_short  # Add 'http://' by default
        
        # Try opening the URL in the default browser
        try:
            webbrowser.open(website_url)
            speak_text(f"Opening the website: {website_url_short}")
        except Exception as e:
            speak_text(f"Failed to open the website. Error: {str(e)}")

    # Get weather information
    def get_weather(self, city_name):
        api_key = "your_api_key"  # Add your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            description = data['weather'][0]['description']
            speak_text(f"The weather in {city_name} is {description} with a temperature of {temperature}°C.")
        else:
            speak_text(f"Could not get weather data for {city_name}.")

    # Check Internet Status
    def check_internet(self):
        try:
            response = requests.get("http://google.com", timeout=5)
            if response.status_code == 200:
                speak_text("You are connected to the internet.")
            else:
                speak_text("No internet connection detected.")
        except requests.ConnectionError:
            speak_text("No internet connection detected.")

    # Check for email (Assuming integration with an email service)
    def check_email(self):
        speak_text("Opening your email client...")
        # You can integrate your email client here, like opening Gmail using webbrowser:
        webbrowser.open("https://mail.google.com")
    
    # Other functionalities like opening a specific page can be added similarly
web_functions = WebFunctions() 


# --*Click on UI with Commands*--

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path

class UIHandler:
    def __init__(self):
        pass

    def write_text(self, text):
        """Simulates typing the given text."""
        pyautogui.write(text, interval=0.05)  # Adjust interval for typing speed

    def ocr_click_on_text(self, target_text):
        # Capture the screen
        screenshot = ImageGrab.grab()
        screenshot_text = pytesseract.image_to_string(screenshot)

        # Check if the target text exists in the screenshot
        if target_text.lower() in screenshot_text.lower():
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            for i in range(len(data['text'])):
                if target_text.lower() == data['text'][i].lower():
                    x = data['left'][i] + data['width'][i] // 2
                    y = data['top'][i] + data['height'][i] // 2
                    pyautogui.click(x, y)
                    print(f"Clicked on text '{target_text}' at position ({x}, {y}).")
                    return True
        print(f"Text '{target_text}' not found on the screen.")
        return False

    def click_on_element(self, element_name):
        try:
            app = Application(backend="uia").connect(title_re=".*", found_index=0)
            dlg = app.active()
            element = dlg.child_window(title=element_name, control_type="Text")
            if element.exists():
                element.click_input()
                print(f"Clicked on {element_name}.")
                return True
            else:
                print(f"Element '{element_name}' not found.")
                return False
        except Exception as e:
            print(f"Error clicking on element '{element_name}': {e}")
            return False

    def find_and_click_text(self, element_name):
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

        for i, text in enumerate(data['text']):
            if element_name.lower() in text.lower():
                x = data['left'][i]
                y = data['top'][i]
                width = data['width'][i]
                height = data['height'][i]
                center_x = x + width // 2
                center_y = y + height // 2
                pyautogui.click(center_x, center_y)
                print(f"Clicked on '{element_name}' at ({center_x}, {center_y}).")
                return True
        print(f"Element '{element_name}' not found.")
        return False

    def click_on(self, target_name):
        """
        Attempts to click on a UI element by name. Falls back to OCR and finally
        to the find_and_click_text method if previous methods fail.
        """
        if self.ocr_click_on_text(target_name):
            return
        elif self.click_on_element(target_name):
            return
        else:
            print(f"Trying find_and_click_text as a last resort for '{target_name}'...")
            self.find_and_click_text(target_name)


ui_handler = UIHandler()  # Instantiate UIHandler



if __name__ == "__main__":
    app = "Notepad"
    ApplicationHandler.open_application(app)
    text_to_write = "How are you"
    ui_handler.write_text(text_to_write)
    print("Text has been written.")



            
            