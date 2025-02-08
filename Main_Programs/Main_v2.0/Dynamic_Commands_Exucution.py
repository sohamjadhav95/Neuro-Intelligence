import re  # Import for cleaning text
from groq import Groq

# Configure the Groq API with your API key
client = Groq(api_key="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")  # Replace with your Groq API key

def Groq_Input(user_input):
    prompt = (
        f"Generate Python code to {user_input}.\n"
        f"User wants to execute this code to complete the activity on a Windows device.\n"
        f"Understand the user's intent and ensure it will complete in code.\n"
        f"Code must be oriented and compatible to execute on Windows 11.\n"
        f"Code must be efficient and fast to execute.\n"
        f"Some tasks may include more than one step process, so make sure the code is compatible to perform multiple steps.\n"
        f"Each process must be visible and show what is happening, not just run in the background.\n"
        f"Ensure the code is executable and prints the code directly.\n"
        f"For web commands, do not use WebDriver. Open and use the browser that is set as the system default.\n"
        f"Do not add explanations or comments."
    )


    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
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
        exit()

    print("Generated Code:\n")
    print(generated_code)

    try:
        print("\nExecuting the Generated Code...\n")
        exec(generated_code)
        print("\nTask completed successfully!")
    except Exception as e:
        print("\nAn error occurred while executing the generated code:")
        print(e)


# Example usage
Groq_Input("search for baby toys and take screenshot of first page and show me that screenshot")
