import time
import csv
import pyttsx3

# In CoreCommands.py
from Core_Functions import ApplicationHandler, System_control, SystemInfromation, FileHandler, WebFunctions
from Core_Functions import WebFunctions, UIHandler
from System_Shortcut_Functions import System_Shortcuts

# Instantiate where needed:
app_handler = ApplicationHandler()
system_control = System_control()
system_information = SystemInfromation()  # Consider renaming this to SystemInformation if needed
file_handler = FileHandler()
web_functions = WebFunctions()
ui_handler = UIHandler()
sys_shortcuts = System_Shortcuts()


# Initialize the recognizer and TTS engine

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




# --*Main Code of Basic Commands*--

commands = {
    "exit": lambda: speak_text("Exiting, Good bye!"),
    
    # UI Access (Click on elements)
    "click on": lambda element_name: ui_handler.click_on(element_name),
    
    # System Information
    "battery status": lambda: system_information.get_battery_status(),
    "cpu usage": lambda: system_information.get_cpu_usage(),
    "internet status": lambda: system_information.check_internet(),

    # Web and Browser Commands
    "check email": lambda: web_functions.check_email(),
    "check internet": lambda: web_functions.check_internet(),
    "get weather": lambda city_name: web_functions.get_weather(city_name),
  
    # System Control
    "increase volume": lambda: system_control.increase_volume(),
    "decrease volume": lambda: system_control.decrease_volume(),
    "mute sound": lambda: system_control.mute_sound(),
    "unmute sound": lambda: system_control.unmute_sound(),
    "sleep mode": lambda: system_control.sleep_mode(),
    "shutdown": lambda: system_control.shutdown(),
    "restart": lambda: system_control.restart(),
    
    # Personal Assistant
    "current date": lambda: speak_text(f"Today’s date is {time.strftime('%B %d, %Y')}."),
    "current time": lambda: system_information.get_current_time(),

    # *Direct Working Windows System_Shortcuts*
     # Window Control
    "close window": lambda: sys_shortcuts.close_current_window(),
    "minimize window": lambda: sys_shortcuts.minimize_window(),
    "maximize window": lambda: sys_shortcuts.maximize_window(),
    "switch window": lambda: sys_shortcuts.switch_window(),
    "snap window left": lambda: sys_shortcuts.snap_window_left(),
    "snap window right": lambda: sys_shortcuts.snap_window_right(),
    "close all windows": lambda: sys_shortcuts.close_all_windows(),
    "open new window": lambda: sys_shortcuts.open_new_window(),
    "minimize all windows": lambda: sys_shortcuts.minimize_all_windows(),
    "restore window": lambda: sys_shortcuts.restore_window(),
    "toggle taskbar visibility": lambda: sys_shortcuts.toggle_taskbar_visibility(),

    # Application Control
    "open task manager": lambda: sys_shortcuts.open_task_manager(),
    "open file explorer": lambda: sys_shortcuts.open_file_explorer(),
    "open command prompt": lambda: sys_shortcuts.open_command_prompt(),
    "open browser": lambda: sys_shortcuts.open_browser(),
    "open notepad": lambda: sys_shortcuts.open_notepad(),
    "open calculator": lambda: sys_shortcuts.open_calculator(),
    "open snipping tool": lambda: sys_shortcuts.open_snipping_tool(),
    "open paint": lambda: sys_shortcuts.open_paint(),
    "open wordpad": lambda: sys_shortcuts.open_wordpad(),
    "open registry editor": lambda: sys_shortcuts.open_registry_editor(),
    "open disk management": lambda: sys_shortcuts.open_disk_management(),
    "open device manager": lambda: sys_shortcuts.open_device_manager(),
    "open event viewer": lambda: sys_shortcuts.open_event_viewer(),

    # Screen Control
    "take screenshot": lambda: sys_shortcuts.take_screenshot(),
    "toggle full screen": lambda: sys_shortcuts.toggle_full_screen(),

    # Lock and Minimize
    "lock computer": lambda: sys_shortcuts.lock_computer(),
    "minimize all windows": lambda: sys_shortcuts.minimize_all_windows(),

    # Virtual Desktop Control
    "create virtual desktop": lambda: sys_shortcuts.create_virtual_desktop(),
    "switch virtual desktop": lambda: sys_shortcuts.switch_virtual_desktop(),

    # Settings Control
    "open settings": lambda: sys_shortcuts.open_settings(),
    "open update settings": lambda: sys_shortcuts.open_update_settings(),
    "open sound settings": lambda: sys_shortcuts.open_sound_settings(),
    "open bluetooth settings": lambda: sys_shortcuts.open_bluetooth_settings(),
    "open wifi settings": lambda: sys_shortcuts.open_wifi_settings(),
    "open keyboard settings": lambda: sys_shortcuts.open_keyboard_settings(),
    "open mouse settings": lambda: sys_shortcuts.open_mouse_settings(),
    "open display settings": lambda: sys_shortcuts.open_display_settings(),
    "open language settings": lambda: sys_shortcuts.open_language_settings(),
    "open time and date settings": lambda: sys_shortcuts.open_time_and_date_settings(),
    "open taskbar settings": lambda: sys_shortcuts.open_taskbar_settings(),
    "open privacy settings": lambda: sys_shortcuts.open_privacy_settings(),
    "open storage settings": lambda: sys_shortcuts.open_storage_settings(),
    "open apps settings": lambda: sys_shortcuts.open_apps_settings(),
    "open power and sleep settings": lambda: sys_shortcuts.open_power_and_sleep_settings(),
    "open default apps settings": lambda: sys_shortcuts.open_default_apps_settings(),
    "open personalization settings": lambda: sys_shortcuts.open_personalization_settings(),
    "open fonts settings": lambda: sys_shortcuts.open_fonts_settings(),
    "open region settings": lambda: sys_shortcuts.open_region_settings(),
    "open accounts settings": lambda: sys_shortcuts.open_accounts_settings(),
    "open backup settings": lambda: sys_shortcuts.open_backup_settings(),
    "open security and maintenance": lambda: sys_shortcuts.open_security_and_maintenance(),
    "open feedback hub": lambda: sys_shortcuts.open_feedback_hub(),
    "open system properties": lambda: sys_shortcuts.open_system_properties(),
    "open network connections": lambda: sys_shortcuts.open_network_connections(),
    "open action center": lambda: sys_shortcuts.open_action_center(),
    "open device encryption settings": lambda: sys_shortcuts.open_device_encryption_settings(),
    "open control panel": lambda: sys_shortcuts.open_control_panel(),
    "open services": lambda: sys_shortcuts.open_services(),

}