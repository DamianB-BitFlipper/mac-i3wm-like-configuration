import subprocess
import json


def run_bash_command(command: str, *, json_output: bool = False) -> dict | None:
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        # Check if the command was successful
        if result.returncode == 0:
            # Parse the JSON output if requested
            if json_output:
                parsed_output = json.loads(result.stdout)
                return parsed_output
            else:
                return None
        else:
            # Handle the case where the command failed
            print(f"Error running command: {result.stderr}")
            return None
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return None
