import csv
import os
from groq import Groq
import pandas as pd

# Get API key from environment variable - REQUIRED for security
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("ERROR: GROQ_API_KEY environment variable not set!")
    print("Please set your Groq API key: export GROQ_API_KEY='your_api_key_here'")
    exit(1)

try:
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# Get the current directory and create relative path for CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(current_dir, "commands_database.csv")

# Initialize CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["No Command"])
        print(f"Created new CSV file: {CSV_FILE}")
    except Exception as e:
        print(f"Error creating CSV file: {e}")


def store_command(command):
    """Append the command to the CSV file."""
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([command])
    except Exception as e:
        print(f"Error storing command: {e}")

def get_last_commands(n=5):
    """Get the last n commands from the CSV file."""
    try:
        if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
            df = pd.read_csv(CSV_FILE)
            if len(df) > 0:
                last_commands = df.tail(n)
                return last_commands.values.tolist()
        return []
    except Exception as e:
        print(f"Error reading last commands: {e}")
        return []

def modify_command_api(user_input):
    """Use the API to modify the command based on recent commands."""
    if not client:
        print("Error: Groq client not available")
        return user_input
        
    last_commands = get_last_commands(5)
    context = last_commands

    prompt = f"""
    You are an AI assistant that refines and clarifies user commands based on context from previous instructions (RAG approach).

    Previous commands from the user:
    {context}

    Current user command: "{user_input}"

    Your task is to:
    1. If the current command references previous commands (e.g., "those columns", "that file", "the same thing"), replace vague references with specific details from the context
    2. Make the command more precise and actionable
    3. Maintain the original intent while adding necessary specificity
    4. If no context is relevant, return the original command unchanged

    Rules:
    - Only return the refined command, no explanations
    - Keep the command concise and clear
    - Preserve the original action/verb
    - Add specific details only when they can be inferred from context

    Refined command:"""

    try:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=100,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        response = completion.choices[0].message.content.strip()
        return response

    except Exception as e:
        print(f"Error modifying command: {e}")
        return user_input

def basic_rag(user_input):
    """Process user input, modify it using API, and store the result."""
    if not user_input or user_input.strip() == "":
        print("Empty input received")
        return None
        
    modified_command = modify_command_api(user_input)
    store_command(modified_command)  # Append only the modified command to CSV
    print(f"Modified command: {modified_command}")
    return modified_command


if __name__ == "__main__":
    user_input = "show me average of both columns"
    modified_command = basic_rag(user_input)

