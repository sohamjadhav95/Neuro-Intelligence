import csv
from groq import Groq
import pandas as pd
import os

client = Groq(api_key="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")

CSV_FILE = r"E:\Projects\Neuro-Intelligence\Main_Programs\Main_v2.7 Rag and Other Improvemts\Retrival_Agumented_Generation\commands_database.csv"

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["No Command"])



def store_command(command):
    """Append the command to the CSV file."""
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([command])

def get_last_commands(n=5):
    last_commands = pd.read_csv(CSV_FILE).tail(n)
    return last_commands.values.tolist()

def modify_command_api(user_input):
    """Use the API to modify the command based on recent commands."""
    last_commands = get_last_commands(5)
    context = last_commands

    prompt = f"""
    You are an AI assistant that refines user commands based on previous instructions Like RAG.
    Here are the last few commands given by the user:
    
    {context}
    
    The user has now given a new command: "{user_input}"
    
    Based on the previous commands, modify the current command to be more precise.
    If the command references previous commands (e.g., 'those columns'), replace the reference with exact details.
    
    Return only the modified command, nothing else.
    """

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
        return f"Error: {str(e)}"

def basic_rag(user_input):
    """Process user input, modify it using API, and store the result."""
    modified_command = modify_command_api(user_input)
    store_command(modified_command)  # Append only the modified command to CSV
    print(f"Modified command: {modified_command}")
    return modified_command


if __name__ == "__main__":
    user_input = "show me average of both columns"
    modified_command = basic_rag(user_input)

