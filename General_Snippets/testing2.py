import os
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyBHzC6HBUW36d9ZIIZEa1Wy30vx7bgchuY")

def main():
    print("Welcome to the Gemini API Code Generator!")
    print("Type your command to generate specific code.")
    print("For example, 'Generate Python code for a function to calculate factorial.'")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("Enter your code request: ").strip()
        if user_input.lower() == "exit":
            print("Exiting the Code Generator. Goodbye!")
            break
        
        print("\nGenerating your code...\n")
        
        # Use the start_chat method for generating code
        try:
            # Tailoring the interaction
            prompt = f"Write only the code for: {user_input}. No explanation or additional text."
            chat_session = genai.start_chat(model="gemini-2.0-flash-exp")
            response = chat_session.send_message(prompt)
            
            generated_code = response.text.strip()
            print("Generated Code:\n")
            print(generated_code)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()
