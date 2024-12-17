import google.generativeai as genai
import re  # Import for cleaning text

# Configure the API with your Gemini API key
genai.configure(api_key="AIzaSyCiQrXmDQFOzlCRWcZdqNyVNH6k7J9BqZ8")  # Replace with your API key

# User input for the desired task
user_input = "create demo.txt file in dowenloads folder"

# Adding a clear prompt to generate code with confirmation messages
prompt = (
    f"Generate Python code to {user_input}. "
    f"The code must include a meaningful confirmation message based on the task outcome, "
    f"such as 'Internet connected successfully' or 'Battery is 80% charged'. "
    f"Do not add explanations or comments. Ensure the code prints the result."
)

# Use the Gemini model to generate content based on the prompt
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Clean the generated code
generated_code = response.text
generated_code = re.sub(r"```[a-zA-Z]*\n|```", "", generated_code).strip()

# Print the cleaned code
print("Generated Code:\n")
print(generated_code)

# Execute the cleaned code
try:
    print("\nExecuting the Generated Code...\n")
    exec(generated_code)
    print("\nTask completed successfully!")
except Exception as e:
    print("\nAn error occurred while executing the generated code:")
    print(e)
