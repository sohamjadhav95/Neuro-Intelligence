import pyttsx3
import time
import pyautogui
import speech_recognition as sr

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
    

class System_Shortcuts:

    # --*Window Control*--
    def close_current_window(self):
        """Close the current window."""
        pyautogui.hotkey("alt", "f4")
        speak_text("Current window closed.")

    def minimize_window(self):
        """Minimize the current window."""
        pyautogui.hotkey("win", "down")
        speak_text("Current window minimized.")

    def maximize_window(self):
        """Maximize the current window."""
        pyautogui.hotkey("win", "up")
        speak_text("Current window maximized.")

    def switch_window(self):
        """Switch to the next open window."""
        pyautogui.hotkey("alt", "tab")
        speak_text("Switched to the next window.")

    def snap_window_left(self):
        """Snap the current window to the left."""
        pyautogui.hotkey("win", "left")
        speak_text("Window snapped to the left.")

    def snap_window_right(self):
        """Snap the current window to the right."""
        pyautogui.hotkey("win", "right")
        speak_text("Window snapped to the right.")
        
    def close_all_windows(self):
        """Close all open windows."""
        pyautogui.hotkey("ctrl", "shift", "esc")
        pyautogui.sleep(1)
        pyautogui.typewrite("taskkill /f /im explorer.exe")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        speak_text("All windows closed.")

    def open_new_window(self):
        """Open a new window of the current application."""
        pyautogui.hotkey("ctrl", "n")
        speak_text("New window opened.")

    def minimize_all_windows(self):
        """Minimize all windows."""
        pyautogui.hotkey("win", "d")
        speak_text("All windows minimized.")

    def restore_window(self):
        """Restore minimized windows."""
        pyautogui.hotkey("win", "d")
        speak_text("Windows restored.")

    def toggle_taskbar_visibility(self):
        """Toggle the visibility of the taskbar."""
        pyautogui.hotkey("win", "t")
        speak_text("Taskbar visibility toggled.")

    # --*Application Control*--
    def open_task_manager(self):
        """Open Task Manager."""
        pyautogui.hotkey("ctrl", "shift", "esc")
        speak_text("Task Manager opened.")

    def open_file_explorer(self):
        """Open File Explorer."""
        pyautogui.hotkey("win", "e")
        speak_text("File Explorer opened.")

    def open_command_prompt(self):
        """Open Command Prompt."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("cmd")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        speak_text("Command Prompt opened.")

    def open_browser(self):
        """Open the default web browser."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("msedge")  # Change to "chrome", "firefox", or your browser name
        pyautogui.press("enter")
        pyautogui.sleep(1)
        speak_text("Default web browser opened.")
        
    def open_notepad(self):
        """Open Notepad."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("notepad")
        pyautogui.press("enter")
        speak_text("Notepad opened.")

    def open_calculator(self):
        """Open Calculator."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("calc")
        pyautogui.press("enter")
        speak_text("Calculator opened.")

    def open_snipping_tool(self):
        """Open Snipping Tool."""
        pyautogui.hotkey("win", "shift", "s")
        speak_text("Snipping Tool opened.")

    def open_paint(self):
        """Open Paint."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("mspaint")
        pyautogui.press("enter")
        speak_text("Paint opened.")

    def open_wordpad(self):
        """Open WordPad."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("wordpad")
        pyautogui.press("enter")
        speak_text("WordPad opened.")

    def open_task_manager(self):
        """Open Task Manager."""
        pyautogui.hotkey("ctrl", "shift", "esc")
        speak_text("Task Manager opened.")

    def open_registry_editor(self):
        """Open Registry Editor."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("regedit")
        pyautogui.press("enter")
        speak_text("Registry Editor opened.")

    def open_disk_management(self):
        """Open Disk Management."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("diskmgmt.msc")
        pyautogui.press("enter")
        speak_text("Disk Management opened.")

    def open_device_manager(self):
        """Open Device Manager."""
        pyautogui.hotkey("win", "x")
        pyautogui.sleep(1)
        pyautogui.press("m")
        speak_text("Device Manager opened.")

    def open_event_viewer(self):
        """Open Event Viewer."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("eventvwr.msc")
        pyautogui.press("enter")
        speak_text("Event Viewer opened.")


    # --*Screen Control*--
    def take_screenshot(self):
        """Take a screenshot."""
        pyautogui.hotkey("win", "prtsc")
        speak_text("Screenshot taken.")

    def toggle_full_screen(self):
        """Toggle full-screen mode for the active application."""
        pyautogui.hotkey("f11")
        speak_text("Full-screen mode toggled.")

    # --*Lock and Minimize*--
    def lock_computer(self):
        """Lock the computer."""
        pyautogui.hotkey("win", "l")
        speak_text("Computer locked.")

    def minimize_all_windows(self):
        """Minimize all open windows."""
        pyautogui.hotkey("win", "d")
        speak_text("All windows minimized.")

    # --*Virtual Desktop Control*--
    def create_virtual_desktop(self):
        """Create a new virtual desktop."""
        pyautogui.hotkey("win", "ctrl", "d")
        speak_text("New virtual desktop created.")

    def switch_virtual_desktop(self):
        """Switch between virtual desktops."""
        pyautogui.hotkey("win", "ctrl", "left")
        speak_text("Switched to the previous virtual desktop.")
        pyautogui.hotkey("win", "ctrl", "right")
        speak_text("Switched to the next virtual desktop.")

    # --*Settings Control*--
    def open_settings(self):
        """Open Windows Settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        speak_text("Settings opened.")

    def open_update_settings(self):
        """Open Windows Update settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("update")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Windows Update settings opened.")

    def open_sound_settings(self):
        """Open Sound Settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("sound")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Sound settings opened.")

    def open_bluetooth_settings(self):
        """Open Bluetooth settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("bluetooth")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Bluetooth settings opened.")

    def open_wifi_settings(self):
        """Open Wi-Fi settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("network status")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Wi-Fi settings opened.")

    def open_keyboard_settings(self):
        """Open Keyboard settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("keyboard")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Keyboard settings opened.")

    def open_mouse_settings(self):
        """Open Mouse settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("mouse")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Mouse settings opened.")

    def open_display_settings(self):
        """Open Display settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("display")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Display settings opened.")

    def open_language_settings(self):
        """Open Language settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("language settings")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Language settings opened.")

    def open_time_and_date_settings(self):
        """Open Time and Date settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("time and date")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Time and date settings opened.")

    def open_taskbar_settings(self):
        """Open Taskbar settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("taskbar")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Taskbar settings opened.")

    def open_privacy_settings(self):
        """Open Privacy settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("privacy settings")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Privacy settings opened.")

    def open_storage_settings(self):
        """Open Storage settings."""
        pyautogui.hotkey("win", "r")  # Open Run dialog
        pyautogui.sleep(2)
        pyautogui.write("ms-settings:storagesense")
        pyautogui.press("enter")
        pyautogui.sleep(2)
        pyautogui.press("tab")  # Navigate focus if required
        pyautogui.press("enter")  # Confirm the action
        print("Storage settings opened.")

    def open_apps_settings(self):
        """Open Apps settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("apps")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        print("Apps settings opened.")

    def open_power_and_sleep_settings(self):
        """Open Power and Sleep settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("power and sleep")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Power and sleep settings opened.")

    def open_default_apps_settings(self):
        """Open Default Apps settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("default apps")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Default apps settings opened.")

    def open_personalization_settings(self):
        """Open Personalization settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("personalization")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Personalization settings opened.")

    def open_fonts_settings(self):
        """Open Fonts settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("fonts")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Fonts settings opened.")

    def open_region_settings(self):
        """Open Region settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("region")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Region settings opened.")

    def open_accounts_settings(self):
        """Open Accounts settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("accounts")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Accounts settings opened.")

    def open_backup_settings(self):
        """Open Backup settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("backup")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Backup settings opened.")

    def open_security_and_maintenance(self):
        """Open Security and Maintenance."""
        pyautogui.hotkey("win", "r")
        pyautogui.typewrite("control /name Microsoft.SecurityAndMaintenance")
        pyautogui.press("enter")
        speak_text("Security and Maintenance opened.")

    def open_feedback_hub(self):
        """Open Feedback Hub."""
        pyautogui.hotkey("win", "f")
        speak_text("Feedback Hub opened.")
        
    def open_system_properties(self):
        """Open System Properties."""
        pyautogui.hotkey("win", "pause")
        speak_text("System Properties opened.")

    def open_network_connections(self):
        """Open Network Connections."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("ncpa.cpl")
        pyautogui.press("enter")
        speak_text("Network Connections opened.")

    def open_taskbar_settings(self):
        """Open Taskbar settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("taskbar")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Taskbar settings opened.")

    def open_action_center(self):
        """Open Action Center."""
        pyautogui.hotkey("win", "a")
        speak_text("Action Center opened.")

    def open_storage_settings(self):
        """Open Storage settings."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(2)
        pyautogui.write("ms-settings:storagesense")
        pyautogui.press("enter")
        pyautogui.sleep(2)
        pyautogui.press("tab")
        pyautogui.press("enter")
        speak_text("Storage settings opened.")

    def open_bluetooth_settings(self):
        """Open Bluetooth settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("bluetooth")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Bluetooth settings opened.")

    def open_device_encryption_settings(self):
        """Open Device Encryption settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("device encryption")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Device Encryption settings opened.")

    def open_control_panel(self):
        """Open Control Panel."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("control")
        pyautogui.press("enter")
        speak_text("Control Panel opened.")

    def open_services(self):
        """Open Services window."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("services.msc")
        pyautogui.press("enter")
        speak_text("Services window opened.")

    def open_event_viewer(self):
        """Open Event Viewer."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("eventvwr.msc")
        pyautogui.press("enter")
        speak_text("Event Viewer opened.")

    def open_remote_desktop_settings(self):
        """Open Remote Desktop settings."""
        pyautogui.hotkey("win", "i")
        pyautogui.sleep(1)
        pyautogui.typewrite("remote desktop")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.press("enter")
        speak_text("Remote Desktop settings opened.")

    def open_virtual_desktop(self):
        """Switch between virtual desktops."""
        pyautogui.hotkey("win", "ctrl", "left")
        pyautogui.sleep(1)
        pyautogui.hotkey("win", "ctrl", "right")
        speak_text("Switched virtual desktop.")       
        
    # --*File Management*--
    def lock_file_or_folder(self):
        """Lock a file or folder using BitLocker (if enabled)."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("control")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.typewrite("bitlocker")
        pyautogui.press("enter")
        speak_text("File or folder locked.")

    def open_file_explorer(self):
        """Open File Explorer."""
        pyautogui.hotkey("win", "e")
        speak_text("File Explorer opened.")

    def open_documents_folder(self):
        """Open Documents folder."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("explorer %userprofile%\\Documents")
        pyautogui.press("enter")
        speak_text("Documents folder opened.")

    def open_downloads_folder(self):
        """Open Downloads folder."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("explorer %userprofile%\\Downloads")
        pyautogui.press("enter")
        speak_text("Downloads folder opened.")

    def open_pictures_folder(self):
        """Open Pictures folder."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("explorer %userprofile%\\Pictures")
        pyautogui.press("enter")
        speak_text("Pictures folder opened.")

    def open_music_folder(self):
        """Open Music folder."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("explorer %userprofile%\\Music")
        pyautogui.press("enter")
        speak_text("Music folder opened.")

    def open_videos_folder(self):
        """Open Videos folder."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("explorer %userprofile%\\Videos")
        pyautogui.press("enter")
        speak_text("Videos folder opened.")
        
        

    # --*Shutdown and Restart*--
    def shutdown_computer(self):
        """Shutdown the computer."""
        pyautogui.hotkey("win", "x")
        pyautogui.sleep(1)
        pyautogui.press("u")
        pyautogui.sleep(1)
        pyautogui.press("u")
        speak_text("Computer shutting down.")

    def restart_computer(self):
        """Restart the computer."""
        pyautogui.hotkey("win", "x")
        pyautogui.sleep(1)
        pyautogui.press("u")
        pyautogui.sleep(1)
        pyautogui.press("r")
        speak_text("Computer restarting.")

    def log_off_user(self):
        """Log off the current user."""
        pyautogui.hotkey("win", "x")
        pyautogui.sleep(1)
        pyautogui.press("u")
        pyautogui.sleep(1)
        pyautogui.press("l")
        speak_text("User logged off.")

    def lock_computer(self):
        """Lock the computer."""
        pyautogui.hotkey("win", "l")
        speak_text("Computer locked.")

    def enable_hibernate_mode(self):
        """Enable Hibernate mode."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("powercfg.cpl")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.typewrite("hibernate")
        pyautogui.press("enter")
        speak_text("Hibernate mode enabled.")

    def enable_sleep_mode(self):
        """Enable Sleep mode."""
        pyautogui.hotkey("win", "r")
        pyautogui.sleep(1)
        pyautogui.typewrite("powercfg.cpl")
        pyautogui.press("enter")
        pyautogui.sleep(1)
        pyautogui.typewrite("sleep")
        pyautogui.press("enter")
        speak_text("Sleep mode enabled.")