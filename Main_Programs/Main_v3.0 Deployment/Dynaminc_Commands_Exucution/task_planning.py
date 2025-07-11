import re
import os
import json
from groq import Groq

# Get API key from environment variable for security
api_key = os.getenv('GROQ_API_KEY', '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')

# Configure the Groq API client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# Predefined commands
argumented_actions = [
    "open application", "close application", "web search", "youtube search", "open website",
    "click on", "write text"
]

general_actions = [
    "battery status", "cpu usage", "internet status",
    "check email", "check internet", "get weather", "increase volume",
    "decrease volume", "mute sound", "unmute sound", "sleep mode",
    "shutdown", "restart", "current date", "current time",
    "close window", "minimize window", "maximize window", "switch window",
    "snap window left", "snap window right", "close all windows", "open new window",
    "minimize all windows", "restore window", "toggle taskbar visibility", "open task manager",
    "open file explorer", "open command prompt", "open browser", "open notepad",
    "open calculator", "open snipping tool", "open paint", "open wordpad",
    "open registry editor", "open disk management", "open device manager", "open event viewer",
    "take screenshot", "toggle full screen", "lock computer", "minimize all windows",
    "create virtual desktop", "switch virtual desktop", "open settings", "open update settings",
    "open sound settings", "open bluetooth settings", "open wifi settings", "open keyboard settings",
    "open mouse settings", "open display settings", "open language settings", "open time and date settings",
    "open taskbar settings", "open privacy settings", "open storage settings", "open apps settings",
    "open power and sleep settings", "open default apps settings", "open personalization settings", "open fonts settings",
    "open region settings", "open accounts settings", "open backup settings", "open security and maintenance",
    "open feedback hub", "open system properties", "open network connections", "open action center",
    "open device encryption settings", "open control panel", "open services"
]

def generate_task_plan(user_input: str) -> dict:
    """Generates a structured task execution plan from user input."""
    if not client:
        print("Error: Groq client not available")
        return {"task": "Error", "steps": []}
        
    prompt = (
        f"User input: {user_input}\n"
        f"Refer these exact action names that are available. Parametric actions: {argumented_actions}, Non-Parametric actions: {general_actions}.\n"
        f"If the action is not available, return the user input directly without a JSON query.\n"
        f"Break down the command into a structured step-by-step plan in JSON format if actions match.\n"
        f"If the action is single step then only return one step.\n"
        f"IMPORTANT: Return ONLY the JSON response, no explanations or additional text.\n"
        f"Each step should have an action and parameters. Use the format:\n"
        f"{{ \"task\": \"Execute multi-step operation\", \"steps\": [\n"
        f"    {{\"step\": 1, \"action\": \"<action1>\", \"parameters\": {{<parameters>}} }},\n"
        f"    {{\"step\": 2, \"action\": \"<action2>\", \"parameters\": {{<parameters>}} }}\n"
        f"]}}\n"
        f"NOTE: For the 'open website' action, the parameter must be 'url' (not 'website'). Always use the exact parameter names as defined in the system's commands dictionary."
    )
   
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1024
        )
    except Exception as e:
        print(f"Error with Groq API: {e}")
        return {"task": "Error", "steps": []}
   
    # Parse response
    generated_text = response.choices[0].message.content.strip()
   
    # First, try to extract JSON from code blocks (if present)
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", generated_text, re.DOTALL)
    if json_match:
        extracted_json = json_match.group(1).strip()
        try:
            task_plan = json.loads(extracted_json)
            print(task_plan)
            return task_plan
        except json.JSONDecodeError as e:
            print(f"JSON decode error from code block: {e}")
            print(f"Extracted content: {extracted_json}")
    
    # If no code block, try to find JSON in the response
    # Look for the first occurrence of a JSON object
    start_idx = generated_text.find('{')
    if start_idx != -1:
        # Find the matching closing brace
        brace_count = 0
        end_idx = start_idx
        
        for i, char in enumerate(generated_text[start_idx:], start_idx):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        if end_idx > start_idx:
            json_str = generated_text[start_idx:end_idx + 1]
            try:
                task_plan = json.loads(json_str)
                print(task_plan)
                return task_plan
            except json.JSONDecodeError as e:
                print(f"JSON decode error from extracted text: {e}")
                print(f"Extracted JSON string: {json_str}")
    
    # If no JSON found in the response, try to parse the whole response as JSON
    try:
        task_plan = json.loads(generated_text)
        print(task_plan)
        return task_plan
    except json.JSONDecodeError:
        print(f"Unexpected Groq API response: {generated_text}")
        return {"task": "Invalid task", "steps": []}
   
# Example usage
if __name__ == "__main__":
    user_input = input("Enter command: ")
    task_plan = generate_task_plan(user_input)
    print(json.dumps(task_plan, indent=4))