
import pyautogui

def open_update_settings():
    """Open Windows Update settings."""
    pyautogui.hotkey("win", "i")
    pyautogui.sleep(1)
    pyautogui.typewrite("update")
    pyautogui.press("enter")
    pyautogui.sleep(1)
    pyautogui.press("enter")
    print("Windows Update settings opened.")

    
open_update_settings()