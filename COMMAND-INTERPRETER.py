import os
import subprocess
import requests
import json
import platform

def translate_command(command):
    # Detect the host operating system
    host_os = platform.system().lower()
    if host_os.startswith("win"):
        host_os = "windows"
    else:
        host_os = "unix"

    # Gemini API configuration
    api_key = "AIzaSyD3PdQngaP01mbPUW48mwk6Ej1gFTr2Ehw"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # Define the prompt
    prompt = (
         f"You are a shell command translator. The host operating system is {host_os}. "
        f"Translate the following command to its equivalent for the host operating system.\n"
        "Return only the final command.\n"
        "Do not add any explanation or additional text.\n"
        f"If the target is Windows, use only PowerShell syntax (no CMD).\n"
        f"Command: {command}"
    )
 
    # Prepare the request payload
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
 
    # Send request to Gemini API
    headers = {'Content-Type': 'application/json'}
    print("Processing your command...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            translated_text = result['candidates'][0]['content']['parts'][0]['text']
            return translated_text.strip()
        else:
            raise Exception("No valid response received from the API")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

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
            execute = input("\n Do you want to execute this command? (y/n): ").strip().lower()
            if execute == 'y':
                print("\nExecuting the command...")
                # Execute the command
                if platform.system().lower().startswith("win"):
                    # Use PowerShell on Windows
                    result = subprocess.run(
                        ["powershell", "-Command", translated_command],
                        capture_output=True,
                        text=True
                    )
                else:
                    # Use the default shell on Unix-based systems
                    result = subprocess.run(
                        translated_command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                print("\nCommand Output:")
                print(result.stdout)
                if result.stderr:
                    print("\nCommand Error:")
                    print(result.stderr)
            else:
                print("\nCommand execution canceled.")
        except Exception as e:
            print(f"An error occurred: {e}")