#!/usr/bin/env python3

import subprocess
import json
import sys


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


def get_space_data_from_uuid(
    yabai_spaces: dict, uuid: str
) -> dict | None:
    for space in yabai_spaces:
        if space["uuid"] == uuid:
            return space

    # The space was not found
    return None


def main():
    # Get the space uuid from the command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <space_uuid>")
        return

    space_uuid = sys.argv[1]

    yabai_spaces = run_bash_command("yabai -m query --spaces", json_output=True)

    if yabai_spaces is None:
        return

    space = get_space_data_from_uuid(yabai_spaces, space_uuid)

    # If the space was found, focus to it
    if space is not None:
        run_bash_command(f"yabai -m space --focus {space['index']}")


if __name__ == "__main__":
    main()
