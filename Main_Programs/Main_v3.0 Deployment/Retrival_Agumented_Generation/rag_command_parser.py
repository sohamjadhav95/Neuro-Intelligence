import csv
import os
from groq import Groq
import pandas as pd

# Get API key from environment variable for security
api_key = os.getenv('GROQ_API_KEY', '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')

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
    """Use the API to modify the command based on recent commands, but only if there is a strict, explicit reference."""
    if not client:
        print("Error: Groq client not available")
        return user_input
        
    last_commands = get_last_commands(5)
    context = last_commands

    prompt = f"""
    You are an AI assistant that refines and clarifies user commands based on context from previous instructions (RAG approach).

    Previous commands from the user:
    {context}

    Current user command: '{user_input}'

    Your task is to:
    1. ONLY modify or inherit from previous commands if the current command contains a STRICT, EXPLICIT reference to them (such as 'that', 'those', 'the same', 'previous', or similar words that clearly indicate a dependency).
    2. If there is NO such explicit reference, treat the current command as a SEPARATE, independent operation and do NOT modify it.
    3. If you do modify, replace vague references with specific details from the context, but ONLY when strictly necessary.
    4. Maintain the original intent and do not add unnecessary context or details.
    5. If no context is relevant, return the original command unchanged.

    Rules:
    - Only return the refined command, no explanations
    - Keep the command concise and clear
    - Preserve the original action/verb
    - Add specific details only when they can be strictly inferred from context

    Refined command:"""

    try:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
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

# New: Generate a natural language output for each command processed

def generate_natural_processing_output(user_command, step=None):
    """Generate a natural language output for the user when processing a task step or command."""
    if not client:
        return f"Processing: {user_command}" if not step else f"Processing step {step}: {user_command}"
    prompt = (
        f"You are an AI assistant.\n"
        f"The user has given the following command: '{user_command}'.\n"
        + (f"This is step {step} of a multi-step task.\n" if step else "") +
        f"Generate a short, friendly, natural language sentence to let the user know what is being done.\n"
        f"Do not use technical jargon.\n"
        f"Be conversational and clear.\n"
        f"Example: 'I'm opening Chrome for you now.' or 'Let me search for the weather.'\n"
        f"Only output the sentence, nothing else."
    )
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=60,
            top_p=0.95,
            stream=False,
            stop=None,
        )
        reply = completion.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print(f"Error generating natural processing output: {e}")
        return f"Processing: {user_command}" if not step else f"Processing step {step}: {user_command}"

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

