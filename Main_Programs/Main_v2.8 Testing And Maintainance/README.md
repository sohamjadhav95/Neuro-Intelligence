# Neuro-Intelligence Main v2.8 - Testing And Maintenance

## Overview
This is a voice-controlled AI assistant system that can perform various Windows system operations, web searches, and application management tasks.

## Recent Bug Fixes and Improvements

### 🔧 Major Bug Fixes

#### 1. **Security Vulnerabilities** ✅ FIXED
- **Fixed**: Hardcoded API keys in multiple files
- **Solution**: API keys now require environment variables - NO FALLBACK KEYS
- **Files**: `Function_Generation.py`, `task_planning.py`, `rag_command_parser.py`
- **Security**: GitHub Push Protection compliant

#### 2. **Path Issues**
- **Fixed**: Hardcoded absolute file paths
- **Solution**: Implemented relative path resolution using `os.path`
- **Files**: `Main_Exucution_Engine.py`, `Core_Commands.py`, `rag_command_parser.py`

#### 3. **Error Handling**
- **Fixed**: Missing try-catch blocks and proper error handling
- **Solution**: Added comprehensive error handling throughout the codebase
- **Files**: All Python files

#### 4. **Duplicate Function Definitions**
- **Fixed**: Duplicate `open_task_manager()` function in `System_Shortcut_Functions.py`
- **Solution**: Removed duplicates and consolidated functionality

#### 5. **CSV File Handling**
- **Fixed**: Improper CSV file initialization and error handling
- **Solution**: Added proper file existence checks and encoding handling
- **File**: `rag_command_parser.py`

#### 6. **TTS Engine Initialization**
- **Fixed**: TTS engine failures could crash the application
- **Solution**: Added graceful fallback when TTS is unavailable
- **Files**: `Core_Commands.py`, `Core_Functions.py`, `System_Shortcut_Functions.py`

#### 7. **Tesseract OCR Path**
- **Fixed**: Hardcoded Tesseract path
- **Solution**: Dynamic path detection for multiple installation locations
- **File**: `Core_Functions.py`

#### 8. **Infinite Loop Prevention**
- **Fixed**: Potential infinite loops in main execution
- **Solution**: Added proper exit conditions and KeyboardInterrupt handling
- **File**: `Main_Exucution_Engine.py`

### 🚀 Improvements Made

#### 1. **Code Structure**
- Better import organization
- Consistent error handling patterns
- Improved function documentation

#### 2. **User Experience**
- Graceful degradation when services are unavailable
- Better error messages and feedback
- Proper exit handling

#### 3. **Maintainability**
- Added requirements.txt for dependency management
- Consistent coding standards
- Better separation of concerns

#### 4. **Portability**
- Relative path resolution
- Environment variable configuration
- Cross-platform compatibility improvements

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables (REQUIRED):**
   ```bash
   # Windows PowerShell
   $env:GROQ_API_KEY="your_groq_api_key_here"
   
   # Windows Command Prompt
   set GROQ_API_KEY=your_groq_api_key_here
   
   # Linux/Mac
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

3. **Install system dependencies:**
   - **Tesseract OCR** (for OCR functionality)
   - **Microphone access** (for voice recognition)

## Usage

### Running the Main Application
```bash
python Main_Exucution_Engine.py
```

### Available Commands

#### System Control
- `increase volume`, `decrease volume`, `mute sound`, `unmute sound`
- `sleep mode`, `shutdown`, `restart`
- `lock computer`, `minimize all windows`

#### Application Management
- `open application [name]`, `close application [name]`
- `open notepad`, `open calculator`, `open browser`, etc.

#### Web Operations
- `web search [query]`, `youtube search [query]`
- `open website [url]`, `check email`

#### System Information
- `battery status`, `cpu usage`, `internet status`
- `current date`, `current time`

#### Window Management
- `close window`, `minimize window`, `maximize window`
- `switch window`, `snap window left/right`

## Architecture

### Core Components

1. **Main_Exucution_Engine.py** - Main entry point and orchestration
2. **Core_Processes/** - Core functionality modules
   - `Core_Commands.py` - Command definitions and mapping
   - `Core_Functions.py` - System operations and utilities
   - `System_Shortcut_Functions.py` - Windows shortcuts and automation
   - `app_paths.py` - Application path management
3. **Dynaminc_Commands_Exucution/** - Dynamic command generation
   - `Function_Generation.py` - AI-powered code generation
   - `task_planning.py` - Task planning and execution
4. **Retrival_Agumented_Generation/** - RAG-based command processing
   - `rag_command_parser.py` - Command enhancement using context

## Troubleshooting

### Common Issues

1. **TTS Engine Not Working**
   - Check if pyttsx3 is properly installed
   - Verify Windows SAPI5 is available
   - Application will continue with text output if TTS fails

2. **Speech Recognition Issues**
   - Ensure microphone access is granted
   - Check internet connection (uses Google Speech API)
   - Verify speech_recognition and pyaudio are installed

3. **OCR Functionality Not Working**
   - Install Tesseract OCR on your system
   - Verify the installation path is correct
   - Check if pytesseract can find the Tesseract executable

4. **API Key Issues** ⚠️ IMPORTANT
   - **REQUIRED**: Set the GROQ_API_KEY environment variable
   - The application will exit if the API key is not set
   - No fallback keys are provided for security reasons
   - Example: `export GROQ_API_KEY="gsk_your_actual_key_here"`

### Error Logging
The application now provides detailed error messages and logging. Check the console output for specific error details.

## Security Notes

### 🔒 API Key Security
- **NEVER** commit API keys to version control
- Use environment variables for all sensitive data
- The application will exit if GROQ_API_KEY is not set
- This prevents accidental exposure of credentials

### 🛡️ GitHub Push Protection
- This codebase is compliant with GitHub's Push Protection
- No hardcoded secrets in the code
- All API keys are properly externalized

## Contributing

When contributing to this project:

1. Follow the existing error handling patterns
2. Use relative paths instead of absolute paths
3. Add proper try-catch blocks for external dependencies
4. Test with missing dependencies to ensure graceful degradation
5. Update the requirements.txt if adding new dependencies
6. **NEVER** add hardcoded API keys or secrets

## License

This project is part of the Neuro-Intelligence system. Please refer to the main project license for usage terms. 