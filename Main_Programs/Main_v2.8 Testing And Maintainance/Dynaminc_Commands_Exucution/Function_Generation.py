import re
import os
from groq import Groq

# Get API key from environment variable - REQUIRED for security
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("ERROR: GROQ_API_KEY environment variable not set!")
    print("Please set your Groq API key: export GROQ_API_KEY='your_api_key_here'")
    exit(1)

# Configure the Groq API with your API key
try:
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

def execute_direct_code_generation(user_input):
    """Fall back to the original direct code generation approach"""
    if not client:
        print("Error: Groq client not available")
        return
        
    prompt = (
        f"Generate Python code to: {user_input}.\n"
        #f"This is Analysis of task: {analyze_task(user_input)} "
        f"User wants to execute this code to complete the activity on a Windows device.\n"
        f"Understand the user's intent and ensure it will complete in code.\n"
        f"Code must be oriented and compatible to execute on Windows 11.\n"
        f"Code must be efficient and fast to execute.\n"
        f"Some tasks may include more than one step process, so make sure the code is compatible to perform multiple steps.\n"
        #f"Each process must be visible and show what is happening, not just run in the background.\n"
        f"Ensure the code is executable and prints the code directly.\n"
        f"For web commands, do not use WebDriver. Open and use the browser that is set as the system default.\n"
        f"Do not add explanations or comments."
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        generated_code = completion.choices[0].message.content

        # Find the first occurrence of a Python code block
        code_match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)

        if code_match:
            generated_code = code_match.group(1).strip()  # Extract the valid Python code
        else:
            print("No valid code detected in response!")
            return

        print("Generated Code:\n")
        print(generated_code)

        try:
            print("\nExecuting the Generated Code...\n")
            exec(generated_code)
            print("\nTask completed successfully!")
        except Exception as e:
            print(f"\nAn error occurred while executing the generated code: {e}")
            print("Reattempting the operation.....")
            Fallback_If_Error(e, prompt, user_input, generated_code)
    except Exception as e:
        print(f"Error generating code: {e}")


def Fallback_If_Error(e, prompt, user_input, generated_code):
    if not client:
        print("Error: Groq client not available for fallback")
        return
        
    prompt_modified = (
        f"This is the error occurred in previous code: {e}\n"
        f"Previous Code: {generated_code}\n"
        f"*Fix This Error And Regenerate Code*\n"
        f"Refer the previous user input and prompt if needed: "
        f"1. user input: {user_input}, 2. prompt: {prompt}"
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_modified}],
            temperature=0.8,
            max_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None,
        )

        generated_code = completion.choices[0].message.content

        # Find the first occurrence of a Python code block
        code_match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)

        if code_match:
            generated_code = code_match.group(1).strip()  # Extract the valid Python code
        else:
            print("No valid code detected in response!")
            return

        print("Generated Code:\n")
        print(generated_code)

        try:
            print("\nExecuting the Generated Code...\n")
            exec(generated_code)
            print("\nTask completed successfully!")
        except Exception as e:
            print(f"\nAn error occurred while executing the generated code: {e}")
    except Exception as e:
        print(f"Error in fallback code generation: {e}")


if __name__ == "__main__":
    # Take user input for testing
    user = "go to website groq console"
    execute_direct_code_generation(user)
    



