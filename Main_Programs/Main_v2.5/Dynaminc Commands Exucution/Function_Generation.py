import re
from groq import Groq

# Configure the Groq API client
client = Groq(api_key="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")

def generate_function(action):
    """Generates a missing function dynamically via API."""
    prompt = f"Generate a Python function for '{action}' including necessary imports."
    try:
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024
        )
        generated_text = response.choices[0].message.content.strip()
        json_match = re.search(r"```(?:python)?\s*([\s\S]*?)\s*```", generated_text, re.DOTALL)
        function_code = json_match.group(1).strip() if json_match else generated_text
        print(function_code)
        exec(function_code, globals())
        print(f"Function '{action}' has been dynamically generated.")
    except Exception as e:
        print(f"[ERROR] Failed to generate function '{action}': {e}")