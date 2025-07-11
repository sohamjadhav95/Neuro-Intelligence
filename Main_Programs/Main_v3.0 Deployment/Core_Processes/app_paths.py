# app_paths.py this is custom module that can use in main code

import os
applications_paths = {
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "paint": r"C:\Windows\System32\mspaint.exe",
    "wordpad": r"C:\Program Files\Windows NT\Accessories\wordpad.exe",
    "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "mozilla firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "microsoft word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "microsoft excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "microsoft powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "vlc media player": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "spotify": r"C:\Users\<YourUsername>\AppData\Roaming\Spotify\Spotify.exe",
    "adobe acrobat reader": r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "discord": r"C:\Users\<YourUsername>\AppData\Local\Discord\app-<version>\Discord.exe",
    "file explorer": r"explorer.exe",
    "windows media player": r"C:\Program Files\Windows Media Player\wmplayer.exe",
    "snipping tool": r"C:\Windows\System32\SnippingTool.exe",
    "task manager": r"C:\Windows\System32\Taskmgr.exe",
    "command prompt": r"C:\Windows\System32\cmd.exe",
    "powershell": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    "control panel": r"C:\Windows\System32\control.exe",
    "settings": r"ms-settings:",
}



def add_custom_app(app_name):
    """
    Adds a custom application path to the applications_paths dictionary, 
    assuming it is located in a common Windows directory.
    """
    # Define a potential path in System32 for the application
    app_path = fr"C:\Windows\System32\{app_name}.exe"
    
    # Add to applications_paths if the path exists
    if os.path.exists(app_path):
        applications_paths[app_name] = app_path
