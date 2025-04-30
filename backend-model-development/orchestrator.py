import subprocess
import sys
import os

# This script executes a sequence of other Python scripts and DVC commands.
# It's designed to automate a daily workflow including data scraping,
# DVC synchronization, and model training.
# The script will stop if any of the commands fail.

# Define the commands to be executed in sequence.
# Ensure these scripts are in your system's PATH or provide their full paths.
# Alternatively, run this script from the directory containing these files.
commands = [
    # Command 1: Run the image scraper script
    # This script is expected to collect new data.
    "python image_scraper_v3_0.py",

    # Command 2: Push data changes to DVC remote
    # This synchronizes the local data changes tracked by DVC with the remote storage.
    "python dvc_push.py", # Assuming dvc_push.py wraps 'dvc push' or similar logic

    # Command 3: Pull data changes from DVC remote
    # This ensures the local data is up-to-date with the remote storage before training.
    "python dvc_pull.py", # Assuming dvc_pull.py wraps 'dvc pull' or similar logic

    # Command 4: Run the model training script
    # This script is expected to train a model using the potentially updated data.
    "python training_with_logs.py"
]

def run_command(command):
    """
    Executes a single shell command and checks for success.

    Args:
        command (str): The command string to execute.

    Returns:
        bool: True if the command succeeded, False otherwise.
    """
    print(f"--> Running command: {command}")
    try:
        # Use subprocess.run to execute the command.
        # shell=True allows executing command strings as in a shell.
        # check=True will raise CalledProcessError if the command returns a non-zero exit code.
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Command output (stdout):")
        print(result.stdout)
        if result.stderr:
            print("Command output (stderr):")
            print(result.stderr)
        print(f"--> Command succeeded: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"--> Error executing command: {command}")
        print(f"    Exit code: {e.returncode}")
        print(f"    Stderr: {e.stderr}")
        print(f"    Stdout: {e.stdout}")
        return False
    except FileNotFoundError:
        print(f"--> Error: Command not found. Make sure '{command.split()[0]}' is in your PATH or provide the full path.")
        return False
    except Exception as e:
        print(f"--> An unexpected error occurred while running '{command}': {e}")
        return False

def main():
    """
    Main function to execute the sequence of commands.
    """
    print("Starting daily automation sequence...")

    for command in commands:
        if not run_command(command):
            print(f"Sequence stopped due to failure of command: {command}")
            sys.exit(1) # Exit with a non-zero status to indicate failure

    print("Daily automation sequence completed successfully.")
    sys.exit(0) # Exit with a zero status to indicate success

if __name__ == "__main__":
    # It's often good practice to change to the project directory
    # before running the scripts, similar to the cron job example.
    # You'll need to uncomment and set the correct path below if needed.
    # project_directory = "/path/to/your/project" # <-- Set your project path here
    # if os.path.exists(project_directory):
    #     print(f"Changing directory to {project_directory}")
    #     os.chdir(project_directory)
    # else:
    #     print(f"Warning: Project directory not found at {project_directory}. Running commands from current directory.")


    main()
