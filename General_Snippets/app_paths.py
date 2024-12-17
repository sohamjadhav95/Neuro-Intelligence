# app_paths.py this is custom module that can use in main code

import os

applications_paths = {
    "Notepad": r"C:\Windows\System32\notepad.exe",
    "Calculator": r"C:\Windows\System32\calc.exe",
    "Paint": r"C:\Windows\System32\mspaint.exe",
    "WordPad": r"C:\Program Files\Windows NT\Accessories\wordpad.exe",
    "Microsoft Edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "Google Chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "Mozilla Firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "Microsoft Word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "Microsoft Excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "Microsoft PowerPoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "VLC Media Player": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "Spotify": r"C:\Users\<YourUsername>\AppData\Roaming\Spotify\Spotify.exe",
    "Adobe Acrobat Reader": r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
    "Steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "Discord": r"C:\Users\<YourUsername>\AppData\Local\Discord\app-<version>\Discord.exe",
    "File Explorer": r"explorer.exe",
    "Windows Media Player": r"C:\Program Files\Windows Media Player\wmplayer.exe",
    "Snipping Tool": r"C:\Windows\System32\SnippingTool.exe",
    "Task Manager": r"C:\Windows\System32\Taskmgr.exe",
    "Command Prompt": r"C:\Windows\System32\cmd.exe",
    "PowerShell": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    "Control Panel": r"C:\Windows\System32\control.exe",
    "Settings": r"ms-settings:",

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
