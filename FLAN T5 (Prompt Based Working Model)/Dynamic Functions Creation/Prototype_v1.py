from transformers import AutoTokenizer, AutoModelForCausalLM

# Use GPT-2 model
model_name = "gpt2"  # You can replace this with another GPT-2 variant, e.g., "gpt2-medium" or "gpt2-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_function_code(user_input):
    """
    Generate Python function code based on the user input task description.
    """
    prompt = (
        f"Generate a Python function for the following task: '{user_input}'. "
        f"The function should include necessary imports, a well-defined function, "
        f"and print the relevant output."
    )
    
    # Tokenize input and generate code
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=512, num_beams=5, early_stopping=True)
    
    # Decode and return the generated code
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_code

# Example usage
user_input = "check the battery status"  # You can change this to any user request
function_code = generate_function_code(user_input)

print("Generated Code:\n")
print(function_code)
