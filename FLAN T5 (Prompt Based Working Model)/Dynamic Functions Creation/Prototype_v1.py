import google.generativeai as genai

# Configure the API with your Gemini API key
genai.configure(api_key="AIzaSyCiQrXmDQFOzlCRWcZdqNyVNH6k7J9BqZ8")

# Define the task prompt for generating Python code
prompt = """
Write a Python function to check the battery status of a computer using the psutil library.
The function should:
1. Get the battery percentage and charging status.
2. Print the results in a readable format.
3. Handle cases where the battery status is unavailable.
Include necessary imports and example usage.
"""

# Use the Gemini model to generate content based on the prompt
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Print the generated code
print("Generated Code:\n")
print(response.text)
