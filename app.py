import os
import sys
import google.generativeai as genai
import subprocess
import re

# Configure the API key
API_KEY = os.environ.get("API")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def greet() -> None:
    print("""
    Hello Kartik,
    What would you like me to do for you!""")

def get_context() -> str:
    return input(">>> ")

def generate_script(context: str) -> str:
    prompt = f"""As an AI assistant, your task is to create a script to accomplish the following: {context}

    Break the context into a series of tasks and then generate a scrip to do it using AppleScript, Python, or Bash.

    Requirements:
    1. Provide ONLY the script code, without any explanations or additional text.
    2. The script should be fully functional and ready to run.
    3. Choose the most appropriate language among AppleScript, Python, or Bash based on the task requirements.
    4. For AppleScript, start the code with "-- AppleScript" on the first line.
    5. If any app on the MAC is asked for se an apple script to compete the program.
    6. For Python, start the code with "# Python" on the first line.
    7. For Bash, start the code with "#!/bin/bash" on the first line.
    8. Ensure the script handles errors gracefully and provides appropriate output or logging.
    9. Optimize the script for efficiency and readability.

    Now, generate the script to accomplish the given task:
    """
    
    response = model.generate_content(prompt)
    content = response._result.candidates[0].content.parts[0].text
    print(content)
    return content

def detect_script_type(script: str) -> str:
    if script.strip().startswith("-- AppleScript"):
        return "applescript"
    elif script.strip().startswith("# Python"):
        return "python"
    elif script.strip().startswith("#!/bin/bash"):
        return "bash"
    else:
        return "unknown"

def execute_applescript(script: str) -> int:
    script = re.sub(r'^-- AppleScript\n', '', script, flags=re.MULTILINE)
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode

def execute_python(script: str) -> int:
    script = re.sub(r'^# Python\n', '', script, flags=re.MULTILINE)
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode

def execute_bash(script: str) -> int:
    script = re.sub(r'^#!/bin/bash\n', '', script, flags=re.MULTILINE)
    result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode

def execute_script(script: str) -> int:
    script_type = detect_script_type(script)
    if script_type == "applescript":
        return execute_applescript(script)
    elif script_type == "python":
        return execute_python(script)
    elif script_type == "bash":
        return execute_bash(script)
    else:
        print("Unknown script type. Cannot execute.")
        return 1

def checkstatus(returncode: int) -> None:
    if returncode == 0:
        print("Process completed successfully.")
    else:
        print(f"Process failed with return code {returncode}.")

def status() -> None:
    print("""
    What would you like me to do for you!""")

def main():
    greet()
    returncode = 1
    while True:
        context = get_context()
        if context.lower() == 'exit':
            break
        while (returncode != 0):
            script = generate_script(context)
            returncode = execute_script(script)
            checkstatus(returncode)
            status()

if __name__ == "__main__":
    main()