
import pyautogui

def close_tabs():

    try:
        pyautogui.hotkey("ctrl", "w")  # For Windows/Linux
        print("The current tab has been closed successfully.")
    except Exception as e:
        print(f"An error occurred while trying to close the tab: {e}")     
        
close_tabs()