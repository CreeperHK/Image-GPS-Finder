import os
import subprocess

def check_ollama_model(model_name: str):
    try:
        os.system('ollama list > nul')
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        output = result.stdout

        # Parse the output to extract installed model names
        lines = output.strip().split('\n')
        installed_model_list = []
        for line in lines[1:]:  # Skip the header line
            parts = line.split()
            if parts:
                model = parts[0].strip().replace(":latest", "")
                installed_model_list.append(model)

        return model_name in installed_model_list

    except FileNotFoundError:
        print("Error: Ollama is not installed or not in the system's PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'ollama list': {e}")
        print(f"Ollama output: {e.stdout}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# Example usage:
if __name__ == "__main__":
    model_to_check = ""
    is_installed = check_ollama_model(model_to_check)
    print(is_installed)

    if is_installed:
        print(f"Model '{model_to_check}' is installed.")
    else:
        print(f"Model '{model_to_check}' is NOT installed.")