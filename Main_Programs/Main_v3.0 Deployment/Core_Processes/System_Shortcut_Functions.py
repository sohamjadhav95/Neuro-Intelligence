import pyttsx3
import time
import pyautogui
import speech_recognition as sr

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
try:
    tts_engine = pyttsx3.init('sapi5')

    # Set properties for TTS engine (optional)
    voices = tts_engine.getProperty('voices')
    if voices:
        tts_engine.setProperty('voices', voices[0].id) # Voice for chat
    tts_engine.setProperty('rate', 200)  # Speed of speech
    tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
except Exception as e:
    print(f"Warning: Could not initialize TTS engine: {e}")
    tts_engine = None

# Function to speak text
def speak_text(text):
    if tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
            time.sleep(1)  # Short delay after speaking
        except Exception as e:
            print(f"TTS Error: {e}")
    else:
        print(f"TTS: {text}")
    

class System_Shortcuts:

    # --*Window Control*--
    def close_current_window(self):
        """Close the current window."""
        try:
            pyautogui.hotkey("alt", "f4")
            speak_text("Current window closed.")
        except Exception as e:
            speak_text(f"Error closing window: {e}")

    def minimize_window(self):
        """Minimize the current window."""
        try:
            pyautogui.hotkey("win", "down")
            speak_text("Current window minimized.")
        except Exception as e:
            speak_text(f"Error minimizing window: {e}")

    def maximize_window(self):
        """Maximize the current window."""
        try:
            pyautogui.hotkey("win", "up")
            speak_text("Current window maximized.")
        except Exception as e:
            speak_text(f"Error maximizing window: {e}")

    def switch_window(self):
        """Switch to the next open window."""
        try:
            pyautogui.hotkey("alt", "tab")
            speak_text("Switched to the next window.")
        except Exception as e:
            speak_text(f"Error switching window: {e}")

    def snap_window_left(self):
        """Snap the current window to the left."""
        try:
            pyautogui.hotkey("win", "left")
            speak_text("Window snapped to the left.")
        except Exception as e:
            speak_text(f"Error snapping window left: {e}")

    def snap_window_right(self):
        """Snap the current window to the right."""
        try:
            pyautogui.hotkey("win", "right")
            speak_text("Window snapped to the right.")
        except Exception as e:
            speak_text(f"Error snapping window right: {e}")
        
    def close_all_windows(self):
        """Close all open windows."""
        try:
            pyautogui.hotkey("ctrl", "shift", "esc")
            pyautogui.sleep(1)
            pyautogui.typewrite("taskkill /f /im explorer.exe")
            pyautogui.press("enter")
            pyautogui.sleep(1)
            speak_text("All windows closed.")
        except Exception as e:
            speak_text(f"Error closing all windows: {e}")

    def open_new_window(self):
        """Open a new window of the current application."""
        try:
            pyautogui.hotkey("ctrl", "n")
            speak_text("New window opened.")
        except Exception as e:
            speak_text(f"Error opening new window: {e}")

    def minimize_all_windows(self):
        """Minimize all windows."""
        try:
            pyautogui.hotkey("win", "d")
            speak_text("All windows minimized.")
        except Exception as e:
            speak_text(f"Error minimizing all windows: {e}")

    def restore_window(self):
        """Restore minimized windows."""
        try:
            pyautogui.hotkey("win", "d")
            speak_text("Windows restored.")
        except Exception as e:
            speak_text(f"Error restoring windows: {e}")

    def toggle_taskbar_visibility(self):
        """Toggle the visibility of the taskbar."""
        try:
            pyautogui.hotkey("win", "t")
            speak_text("Taskbar visibility toggled.")
        except Exception as e:
            speak_text(f"Error toggling taskbar: {e}")

    # --*Application Control*--
    def open_task_manager(self):
        """Open Task Manager."""
        try:
            pyautogui.hotkey("ctrl", "shift", "esc")
            speak_text("Task Manager opened.")
        except Exception as e:
            speak_text(f"Error opening Task Manager: {e}")

    def open_file_explorer(self):
        """Open File Explorer."""
        try:
            pyautogui.hotkey("win", "e")
            speak_text("File Explorer opened.")
        except Exception as e:
            speak_text(f"Error opening File Explorer: {e}")

    def open_command_prompt(self):
        """Open Command Prompt."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("cmd")
            pyautogui.press("enter")
            pyautogui.sleep(1)
            speak_text("Command Prompt opened.")
        except Exception as e:
            speak_text(f"Error opening Command Prompt: {e}")

    def open_browser(self):
        """Open the default web browser."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("msedge")  # Change to "chrome", "firefox", or your browser name
            pyautogui.press("enter")
            pyautogui.sleep(1)
            speak_text("Default web browser opened.")
        except Exception as e:
            speak_text(f"Error opening browser: {e}")
        
    def open_notepad(self):
        """Open Notepad."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("notepad")
            pyautogui.press("enter")
            speak_text("Notepad opened.")
        except Exception as e:
            speak_text(f"Error opening Notepad: {e}")

    def open_calculator(self):
        """Open Calculator."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("calc")
            pyautogui.press("enter")
            speak_text("Calculator opened.")
        except Exception as e:
            speak_text(f"Error opening Calculator: {e}")

    def open_snipping_tool(self):
        """Open Snipping Tool."""
        try:
            pyautogui.hotkey("win", "shift", "s")
            speak_text("Snipping Tool opened.")
        except Exception as e:
            speak_text(f"Error opening Snipping Tool: {e}")

    def open_paint(self):
        """Open Paint."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("mspaint")
            pyautogui.press("enter")
            speak_text("Paint opened.")
        except Exception as e:
            speak_text(f"Error opening Paint: {e}")

    def open_wordpad(self):
        """Open WordPad."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("wordpad")
            pyautogui.press("enter")
            speak_text("WordPad opened.")
        except Exception as e:
            speak_text(f"Error opening WordPad: {e}")

    def open_registry_editor(self):
        """Open Registry Editor."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("regedit")
            pyautogui.press("enter")
            speak_text("Registry Editor opened.")
        except Exception as e:
            speak_text(f"Error opening Registry Editor: {e}")

    def open_disk_management(self):
        """Open Disk Management."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("diskmgmt.msc")
            pyautogui.press("enter")
            speak_text("Disk Management opened.")
        except Exception as e:
            speak_text(f"Error opening Disk Management: {e}")

    def open_device_manager(self):
        """Open Device Manager."""
        try:
            pyautogui.hotkey("win", "x")
            pyautogui.sleep(1)
            pyautogui.press("m")
            speak_text("Device Manager opened.")
        except Exception as e:
            speak_text(f"Error opening Device Manager: {e}")

    def open_event_viewer(self):
        """Open Event Viewer."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("eventvwr.msc")
            pyautogui.press("enter")
            speak_text("Event Viewer opened.")
        except Exception as e:
            speak_text(f"Error opening Event Viewer: {e}")


    # --*Screen Control*--
    def take_screenshot(self):
        """Take a screenshot."""
        try:
            pyautogui.hotkey("win", "prtsc")
            speak_text("Screenshot taken.")
        except Exception as e:
            speak_text(f"Error taking screenshot: {e}")

    def toggle_full_screen(self):
        """Toggle full-screen mode for the active application."""
        try:
            pyautogui.hotkey("f11")
            speak_text("Full-screen mode toggled.")
        except Exception as e:
            speak_text(f"Error toggling full screen: {e}")

    # --*Lock and Minimize*--
    def lock_computer(self):
        """Lock the computer."""
        try:
            pyautogui.hotkey("win", "l")
            speak_text("Computer locked.")
        except Exception as e:
            speak_text(f"Error locking computer: {e}")

    def create_virtual_desktop(self):
        """Create a new virtual desktop."""
        try:
            pyautogui.hotkey("win", "ctrl", "d")
            speak_text("New virtual desktop created.")
        except Exception as e:
            speak_text(f"Error creating virtual desktop: {e}")

    def switch_virtual_desktop(self):
        """Switch between virtual desktops."""
        try:
            pyautogui.hotkey("win", "ctrl", "left")  # Switch to previous desktop
            # Or use "right" to switch to next desktop
            speak_text("Switched virtual desktop.")
        except Exception as e:
            speak_text(f"Error switching virtual desktop: {e}")

    # --*Settings Control*--
    def open_settings(self):
        """Open Windows Settings."""
        try:
            pyautogui.hotkey("win", "i")
            speak_text("Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Settings: {e}")

    def open_update_settings(self):
        """Open Windows Update Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("update")
            pyautogui.press("enter")
            speak_text("Update Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Update Settings: {e}")

    def open_sound_settings(self):
        """Open Sound Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("sound")
            pyautogui.press("enter")
            speak_text("Sound Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Sound Settings: {e}")

    def open_bluetooth_settings(self):
        """Open Bluetooth Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("bluetooth")
            pyautogui.press("enter")
            speak_text("Bluetooth Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Bluetooth Settings: {e}")

    def open_wifi_settings(self):
        """Open WiFi Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("wifi")
            pyautogui.press("enter")
            speak_text("WiFi Settings opened.")
        except Exception as e:
            speak_text(f"Error opening WiFi Settings: {e}")

    def open_keyboard_settings(self):
        """Open Keyboard Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("keyboard")
            pyautogui.press("enter")
            speak_text("Keyboard Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Keyboard Settings: {e}")

    def open_mouse_settings(self):
        """Open Mouse Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("mouse")
            pyautogui.press("enter")
            speak_text("Mouse Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Mouse Settings: {e}")

    def open_display_settings(self):
        """Open Display Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("display")
            pyautogui.press("enter")
            speak_text("Display Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Display Settings: {e}")

    def open_language_settings(self):
        """Open Language Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("language")
            pyautogui.press("enter")
            speak_text("Language Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Language Settings: {e}")

    def open_time_and_date_settings(self):
        """Open Time and Date Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("time")
            pyautogui.press("enter")
            speak_text("Time and Date Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Time and Date Settings: {e}")

    def open_taskbar_settings(self):
        """Open Taskbar Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("taskbar")
            pyautogui.press("enter")
            speak_text("Taskbar Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Taskbar Settings: {e}")

    def open_privacy_settings(self):
        """Open Privacy Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("privacy")
            pyautogui.press("enter")
            speak_text("Privacy Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Privacy Settings: {e}")

    def open_storage_settings(self):
        """Open Storage Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("storage")
            pyautogui.press("enter")
            speak_text("Storage Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Storage Settings: {e}")

    def open_apps_settings(self):
        """Open Apps Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("apps")
            pyautogui.press("enter")
            speak_text("Apps Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Apps Settings: {e}")

    def open_power_and_sleep_settings(self):
        """Open Power and Sleep Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("power")
            pyautogui.press("enter")
            speak_text("Power and Sleep Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Power and Sleep Settings: {e}")

    def open_default_apps_settings(self):
        """Open Default Apps Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("default apps")
            pyautogui.press("enter")
            speak_text("Default Apps Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Default Apps Settings: {e}")

    def open_personalization_settings(self):
        """Open Personalization Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("personalization")
            pyautogui.press("enter")
            speak_text("Personalization Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Personalization Settings: {e}")

    def open_fonts_settings(self):
        """Open Fonts Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("fonts")
            pyautogui.press("enter")
            speak_text("Fonts Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Fonts Settings: {e}")

    def open_region_settings(self):
        """Open Region Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("region")
            pyautogui.press("enter")
            speak_text("Region Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Region Settings: {e}")

    def open_accounts_settings(self):
        """Open Accounts Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("accounts")
            pyautogui.press("enter")
            speak_text("Accounts Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Accounts Settings: {e}")

    def open_backup_settings(self):
        """Open Backup Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("backup")
            pyautogui.press("enter")
            speak_text("Backup Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Backup Settings: {e}")

    def open_security_and_maintenance(self):
        """Open Security and Maintenance."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("wscui.cpl")
            pyautogui.press("enter")
            speak_text("Security and Maintenance opened.")
        except Exception as e:
            speak_text(f"Error opening Security and Maintenance: {e}")

    def open_feedback_hub(self):
        """Open Feedback Hub."""
        try:
            pyautogui.hotkey("win", "f")
            speak_text("Feedback Hub opened.")
        except Exception as e:
            speak_text(f"Error opening Feedback Hub: {e}")

    def open_system_properties(self):
        """Open System Properties."""
        try:
            pyautogui.hotkey("win", "pause")
            speak_text("System Properties opened.")
        except Exception as e:
            speak_text(f"Error opening System Properties: {e}")

    def open_network_connections(self):
        """Open Network Connections."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("ncpa.cpl")
            pyautogui.press("enter")
            speak_text("Network Connections opened.")
        except Exception as e:
            speak_text(f"Error opening Network Connections: {e}")

    def open_action_center(self):
        """Open Action Center."""
        try:
            pyautogui.hotkey("win", "a")
            speak_text("Action Center opened.")
        except Exception as e:
            speak_text(f"Error opening Action Center: {e}")

    def open_device_encryption_settings(self):
        """Open Device Encryption Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("device encryption")
            pyautogui.press("enter")
            speak_text("Device Encryption Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Device Encryption Settings: {e}")

    def open_control_panel(self):
        """Open Control Panel."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("control")
            pyautogui.press("enter")
            speak_text("Control Panel opened.")
        except Exception as e:
            speak_text(f"Error opening Control Panel: {e}")

    def open_services(self):
        """Open Services."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("services.msc")
            pyautogui.press("enter")
            speak_text("Services opened.")
        except Exception as e:
            speak_text(f"Error opening Services: {e}")

    def open_remote_desktop_settings(self):
        """Open Remote Desktop Settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("remote desktop")
            pyautogui.press("enter")
            speak_text("Remote Desktop Settings opened.")
        except Exception as e:
            speak_text(f"Error opening Remote Desktop Settings: {e}")

    def open_virtual_desktop(self):
        """Open Virtual Desktop settings."""
        try:
            pyautogui.hotkey("win", "i")
            pyautogui.sleep(1)
            pyautogui.typewrite("virtual desktop")
            pyautogui.press("enter")
            speak_text("Virtual Desktop settings opened.")
        except Exception as e:
            speak_text(f"Error opening Virtual Desktop settings: {e}")

    def lock_file_or_folder(self):
        """Lock a file or folder (placeholder for future implementation)."""
        try:
            speak_text("File or folder locking functionality not yet implemented.")
        except Exception as e:
            speak_text(f"Error with file locking: {e}")

    def open_documents_folder(self):
        """Open Documents folder."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("shell:Documents")
            pyautogui.press("enter")
            speak_text("Documents folder opened.")
        except Exception as e:
            speak_text(f"Error opening Documents folder: {e}")

    def open_downloads_folder(self):
        """Open Downloads folder."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("shell:Downloads")
            pyautogui.press("enter")
            speak_text("Downloads folder opened.")
        except Exception as e:
            speak_text(f"Error opening Downloads folder: {e}")

    def open_pictures_folder(self):
        """Open Pictures folder."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("shell:Pictures")
            pyautogui.press("enter")
            speak_text("Pictures folder opened.")
        except Exception as e:
            speak_text(f"Error opening Pictures folder: {e}")

    def open_music_folder(self):
        """Open Music folder."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("shell:Music")
            pyautogui.press("enter")
            speak_text("Music folder opened.")
        except Exception as e:
            speak_text(f"Error opening Music folder: {e}")

    def open_videos_folder(self):
        """Open Videos folder."""
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.sleep(1)
            pyautogui.typewrite("shell:Videos")
            pyautogui.press("enter")
            speak_text("Videos folder opened.")
        except Exception as e:
            speak_text(f"Error opening Videos folder: {e}")

    def shutdown_computer(self):
        """Shutdown the computer."""
        try:
            pyautogui.hotkey("alt", "f4")
            pyautogui.sleep(1)
            pyautogui.press("down")
            pyautogui.press("enter")
            speak_text("Computer shutdown initiated.")
        except Exception as e:
            speak_text(f"Error shutting down computer: {e}")

    def restart_computer(self):
        """Restart the computer."""
        try:
            pyautogui.hotkey("alt", "f4")
            pyautogui.sleep(1)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            speak_text("Computer restart initiated.")
        except Exception as e:
            speak_text(f"Error restarting computer: {e}")

    def log_off_user(self):
        """Log off the current user."""
        try:
            pyautogui.hotkey("alt", "f4")
            pyautogui.sleep(1)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            speak_text("User log off initiated.")
        except Exception as e:
            speak_text(f"Error logging off user: {e}")

    def enable_hibernate_mode(self):
        """Enable hibernate mode."""
        try:
            pyautogui.hotkey("alt", "f4")
            pyautogui.sleep(1)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            speak_text("Hibernate mode enabled.")
        except Exception as e:
            speak_text(f"Error enabling hibernate mode: {e}")

    def enable_sleep_mode(self):
        """Enable sleep mode."""
        try:
            pyautogui.hotkey("alt", "f4")
            pyautogui.sleep(1)
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("down")
            pyautogui.press("enter")
            speak_text("Sleep mode enabled.")
        except Exception as e:
            speak_text(f"Error enabling sleep mode: {e}")