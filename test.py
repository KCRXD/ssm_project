from huggingface_hub import InferenceClient

def translate_command(command):
    # Initialize the Hugging Face Inference Client
    client = InferenceClient(
        provider="novita",
        api_key="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" 
    )

    # Define the prompt
    prompt = (
        "You are a linux-windows shell interpreter that can only answer back with commands, so no explanation of the commands can be returned by you. Detect the source operating system (Unix/Linux/macOS or Windows) "
        "based on the following command and provide its equivalent for the other operating system.\n"
        f"Command: {command}\n"
        "Return only the final command."
        "please only return the command without any explanation.\n"
        "If the command is not valid, return 'Invalid command'.\n"
        "Or when a command is missing options, return the equivalent to the other OS without options as well.\n"
    )

    # Send the request to the model
    print("Processing your command...")
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-Prover-V2-671B",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    # Extract and return the response
    return completion.choices[0].message["content"].strip()

if __name__ == "__main__":
    # Get user input
    user_command = input("Enter your shell command (e.g., ls -l): ").strip()
    if not user_command:
        print("Please enter a valid command.")
    else:
        try:
            translated_command = translate_command(user_command)
            print("\nTranslated Command:")
            print(translated_command)
        except Exception as e:
            print(f"An error occurred: {e}")