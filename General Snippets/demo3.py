import google.generativeai as genai

# Configure the API with your Gemini API key
genai.configure(api_key="AIzaSyCiQrXmDQFOzlCRWcZdqNyVNH6k7J9BqZ8")

user_input = "search cat "

# Define the task prompt for generating Python code
prompt = f"""
You are a command and argument extraction model.
You have to extract command from {user_input}
and also the argument from {user_input}.
1. command must mathch the following:
open application
close application
web search
youtube search
open website

2. arguments are dynamic:
can contain any app name
any search argument 
and website name

Now you have to return extracted command then extract argument in a single line.
eg.
open application chrome
web search current global trends
close application microsoft store
open website youtube.com

(Note: Make Sure You Are Providing The accurate Response for any command and it must stick to rules.)
"""

# Use the Gemini model to generate content based on the prompt
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

def commands_arguments_extracted():
    print(response.text)
    return response.text

commands_arguments_extracted()