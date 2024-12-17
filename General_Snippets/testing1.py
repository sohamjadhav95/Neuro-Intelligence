import pygetwindow as gw
from pywinauto import Application
import subprocess
import psutil

class ApplicationHandler:
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

# Example usage
def speak_text(message):
    print(message)  # Replace this with your text-to-speech logic

app_handler = ApplicationHandler()
app_handler.close_application("microsoft store")  # Replace with the desired app name
