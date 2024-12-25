import google.generativeai as genai
import re  # Import for cleaning text

# Configure the API with your Gemini API key
genai.configure(api_key="AIzaSyCiQrXmDQFOzlCRWcZdqNyVNH6k7J9BqZ8")  # Replace with your API key

def Gemini_Input(user_input):

    prompt = (
        f"Generate Python code to {user_input}. "
        f"Understand the users intent and ensure it will complete in code."
        f"The code must include a meaningful confirmation message based on the task outcome."
        f"Code must be oriented and compatible to exucute on windows 11."
        f"Code must be Efficient and Fast to execute."
        f"Some tasks may include more than one step process so make sure the code comaptible to perform multiple steps."
        f"Ensure the code is executable and prints the results directly. "
        f"Do not add explanations or comments. Ensure the code prints the result."   
    )

    # Use the Gemini model to generate content based on the prompt
    model = genai.GenerativeModel("gemini-1.5-pro")
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
