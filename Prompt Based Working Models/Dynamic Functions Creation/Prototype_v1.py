import google.generativeai as genai

# Configure the API with your Gemini API key
genai.configure(api_key="AIzaSyCiQrXmDQFOzlCRWcZdqNyVNH6k7J9BqZ8")

user_input = "Cheak Battery Status"

# Define the task prompt for generating Python code
prompt = f"""
Write a Python function for {user_input}.
The function should:
1. Include Necessary Imports.
2. Clean Code without errors.
3. Handle dynamic requirmets for generating code based on target for code.
Include necessary imports and example usage.
"""

# Use the Gemini model to generate content based on the prompt
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Print the generated code
print("Generated Code:\n")
print(response.text)
