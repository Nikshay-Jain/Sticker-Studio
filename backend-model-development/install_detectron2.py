import subprocess
import sys

def run_setup_commands():
    """
    Runs git clone for Detectron2 and then installs it in editable mode.
    Prints a success message if both commands complete successfully.
    Output/errors from the commands will typically show in the terminal directly.
    """
    commands = [
        ["git", "clone", "https://github.com/facebookresearch/detectron2.git"],
        [sys.executable, "-m", "pip", "install", "-e", "detectron2"]
        # Using sys.executable ensures we use the 'python' that ran the script
    ]

    print("Attempting to clone Detectron2 and install it...")

    for command in commands:
        command_str = ' '.join(command)
        # We're not logging, but maybe print which command is starting?
        # Let's keep it quiet unless there's a failure, as requested.

        try:
            # Using subprocess.run to execute the command.
            # stdout and stderr are NOT explicitly captured here,
            # so they will go directly to the terminal by default.
            # check=True will raise CalledProcessError if the command fails.
            subprocess.run(
                command,
                check=True # Exit and raise exception if command fails
                # If you wanted to suppress command output, you could add:
                # stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                # But the request is for no logging, minimal output, success signal only.
                # Letting the command output flow is simplest here.
            )
            # If check=True didn't raise an exception, the command succeeded.
            # No need to print success for each command, just the final one.

        except FileNotFoundError:
            # This happens if 'git' or 'python' (via sys.executable) isn't found
            cmd_name = command[0] if len(command) > 0 else "Unknown command"
            print(f"FATAL ERROR: Command '{cmd_name}' not found.", file=sys.stderr)
            print(f"Please ensure '{cmd_name}' is installed and in your system's PATH.", file=sys.stderr)
            sys.exit(1) # Exit on failure

        except subprocess.CalledProcessError as e:
            # This happens if the command runs but returns a non-zero exit code (i.e., fails)
            command_str_failed = ' '.join(e.cmd) # Use e.cmd for the actual command run
            print(f"FATAL ERROR: Command failed with exit code {e.returncode}:", file=sys.stderr)
            print(command_str_failed, file=sys.stderr)
            # The stdout/stderr from the failed command might have already printed
            # because we didn't capture them. If you uncommented capture_output above,
            # you would print e.stdout and e.stderr here.
            sys.exit(e.returncode) # Exit with the same error code as the failed command

        except Exception as e:
            # Catch any other unexpected errors during command execution
            command_str_error = ' '.join(command)
            print(f"FATAL ERROR: An unexpected error occurred while running '{command_str_error}': {e}", file=sys.stderr)
            sys.exit(1) # Exit with a general error code


    # If the loop completes without any exceptions, both commands succeeded
    print("\nSuccess: Detectron2 cloned and installed in editable mode!")

# --- Main Execution ---
if __name__ == "__main__":
    run_setup_commands()
