from predict import predict_command

if __name__ == "__main__":
    print("Welcome to the Command Processor!")
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        main_cmd, arg = predict_command(user_input)
        print(f"Predicted Main Command: {main_cmd}")
        print(f"Predicted Argument: {arg}")
