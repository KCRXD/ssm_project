import os
import subprocess
from huggingface_hub import InferenceClient

def translate_command(command):
    # Initialize the Hugging Face Inference Client
    client = InferenceClient(
        provider="novita",
        api_key="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", 
    )

    # Define the prompt
    prompt = (
        f"You are a linux-windows shell command translator. Detect the source operating system (Unix/Linux/macOS or Windows) "
        f"based on the following command and provide its equivalent for the other operating system.\n"
        f"Command: {command}\n"
        "Return only the final command.\n"
        "Please keep the command as short as possible and do not add any explanation or additional text.\n"
        "my goal is to run the command i get from you so it won't work if you add any explanation or additional text.\n"
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
        # Prompt the user to execute the command
            execute = input("\nDo you want to execute this command? (y/n): ").strip().lower()
            if execute == 'y':
                print("\nExecuting the command...")
                # Execute the command
                result = subprocess.run(translated_command, shell=True, capture_output=True, text=True)
                print("\nCommand Output:")
                print(result.stdout)
                if result.stderr:
                    print("\nCommand Error:")
                    print(result.stderr)
            else:
                print("\nCommand execution canceled.")
        except Exception as e:
            print(f"An error occurred: {e}")