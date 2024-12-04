# Keyword to Command Mapping
keyword_to_command = {
    "open": "open application",
    "delete": "delete file",
    "move": "move file",
    "rename": "rename file",
    "search": "web search",
    "play": "youtube search",
    "make": "create folder"
}

def execute_command(user_input):
    """
    Analyze user input, map keywords to commands, and extract arguments.
    """
    # Normalize user input (case-insensitive matching)
    user_input = user_input.lower()

    # Find the keyword in the user input
    for keyword, command in keyword_to_command.items():
        if user_input.startswith(keyword):
            # Map keyword to command and extract argument
            argument = user_input[len(keyword):].strip()

            # Combine command and argument
            full_command = f"{command} {argument}"
            
            print(f"Predicted Command: {full_command}")
            
            return full_command

    # If no match is found
    print("No matching command found.")
    return None

# User input
command = input("Enter command: ")
execute_command(command)
