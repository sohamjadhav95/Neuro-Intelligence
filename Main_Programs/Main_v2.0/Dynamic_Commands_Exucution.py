import re  # Import for cleaning text
from groq import Groq

# Configure the Groq API with your API key
client = Groq(api_key="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")  # Replace with your Groq API key

def analyze_task(user_input):
    """Break down user input into discrete steps for execution"""
    prompt = (
        f"Analyze this task: '{user_input}'\n"
        f"Break it down into a numbered list of sequential steps needed to complete this task on Windows 11.\n"
        f"Be specific and thorough. Each step should be a discrete action that can be coded.\n"
        f"Format the output as a numbered list only, with no additional text."
    )
    
    completion = client.chat.completions.create(
        model="qwen-2.5-coder-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1024,
        top_p=0.95,
        stream=False,
        stop=None,
    )
    
    steps_text = completion.choices[0].message.content
    
    # Extract the steps into a list
    steps = []
    for line in steps_text.strip().split('\n'):
        # Extract numbered steps (1. Step description)
        match = re.match(r'^\d+\.\s+(.+)$', line)
        if match:
            steps.append(match.group(1).strip())
    
    return steps

def generate_code_for_step(step):
    """Generate code for a specific step"""
    prompt = (
        f"Generate Python code to perform this specific step: '{step}'.\n"
        f"The code will run on Windows 11.\n"
        f"Code must be efficient and compatible with Windows.\n"
        f"Make the process visible to show progress to the user.\n"
        f"For web operations, use the system default browser, not WebDriver.\n"
        f"Return only executable Python code with no explanations or markdown."
    )
    
    completion = client.chat.completions.create(
        model="qwen-2.5-coder-32b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=2048,
        top_p=0.95,
        stream=False,
        stop=None,
    )
    
    generated_code = completion.choices[0].message.content
    
    # Clean up the code - remove markdown code blocks if present
    code_match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)
    if code_match:
        generated_code = code_match.group(1).strip()
    
    return generated_code

def Groq_Input(user_input):
    # Break down the task into steps
    print(f"Analyzing task: {user_input}")
    steps = analyze_task(user_input)
    
    if not steps:
        print("Could not analyze the task into steps. Falling back to direct code generation.")
        execute_direct_code_generation(user_input)
        return
    
    # Display the steps
    print("\nTask has been broken down into these steps:")
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    # Process each step
    for i, step in enumerate(steps, 1):
        print(f"\n[Step {i}/{len(steps)}] {step}")
        generated_code = generate_code_for_step(step)
        
        print(f"Generated Code for Step {i}:\n")
        print(generated_code)
        
        try:
            print(f"\nExecuting Step {i}...\n")
            exec(generated_code)
            print(f"Step {i} completed successfully!")
        except Exception as e:
            print(f"\nAn error occurred in Step {i}:")
            print(e)
            print("Attempting to fix and retry this step...")
            fix_and_retry_step(e, step, generated_code)
    
    print("\nAll steps completed! Task execution finished.")

def execute_direct_code_generation(user_input):
    """Fall back to the original direct code generation approach"""
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
        model="qwen-2.5-coder-32b",
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
        print("Reattempting the operation.....")
        Fallback_If_Error(e, prompt, user_input, generated_code)

def fix_and_retry_step(error, step, previous_code):
    """Attempt to fix and retry a specific step that failed"""
    prompt = (
        f"Error when executing code for this step: '{step}'\n"
        f"The error was: {error}\n"
        f"Previous code that failed: \n{previous_code}\n\n"
        f"Fix this code to properly complete the step. Make it more robust.\n"
        f"Return only the corrected Python code with no explanations."
    )

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=2048,
        top_p=0.95,
        stream=False,
        stop=None,
    )

    fixed_code = completion.choices[0].message.content
    
    # Clean up the code - remove markdown code blocks if present
    code_match = re.search(r"```python\n(.*?)\n```", fixed_code, re.DOTALL)
    if code_match:
        fixed_code = code_match.group(1).strip()
    
    print("Fixed Code:\n")
    print(fixed_code)

    try:
        print("\nExecuting the Fixed Code...\n")
        exec(fixed_code)
        print("\nStep completed successfully after fixing!")
    except Exception as e:
        print("\nError persists after code fix:")
        print(e)
        print("Skipping this step and continuing with the next steps.")

def Fallback_If_Error(e, prompt, user_input, generated_code):
    prompt_modified = (
        f"This is the error occurred in previous code: {e}\n"
        f"Previous Code: {generated_code}\n"
        f"*Fix This Error And Regenerate Code*\n"
        f"Refer the previous user input and prompt if needed: "
        f"1. user input: {user_input}, 2. prompt: {prompt}"
    )

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt_modified}],
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



if __name__ == "__main__":
    # Test cases with different complexity levels
    print("=== Testing Dynamic Command Execution System ===\n")
    
    # Test 1: Simple task
    print("Test 1: Simple task")
    test_input = "create a text file named test.txt and write 'Hello World' in it"
    Groq_Input(test_input)
    print("\n" + "="*50 + "\n")


