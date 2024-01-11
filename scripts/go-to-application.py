#!/usr/bin/env python3

import sys
from script_utils import run_bash_command


def get_window_data_from_application_name(
    yabai_windows: dict, application_name: str
) -> dict | None:
    for window in yabai_windows:
        if window["app"] == application_name:
            return window

    # The application was not found
    return None


def main():
    # Get the application name from the command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <app_name>")
        return

    app_name = sys.argv[1]

    yabai_windows = run_bash_command("yabai -m query --windows", json_output=True)

    if yabai_windows is None:
        return

    window = get_window_data_from_application_name(yabai_windows, app_name)

    # If the window was found, focus to it
    if window is not None:
        run_bash_command(f"yabai -m space --focus {window['space']}")


if __name__ == "__main__":
    main()
