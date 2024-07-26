#!/usr/bin/env python3

# NOTE: On reboot, you may get an error that:
# `Error running command: cannot focus space due to an error with the scripting-addition.`
#
# To fix this, you need to run the following commands:
# `sudo yabai --uninstall-sa`
# `sudo yabai --load-sa`
# `sudo yabai --load-sa` ## Run this command twice for some reason
#
# Follow https://github.com/koekeishiya/yabai/issues/1158 for more info.

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
    # Get the application names from the command line arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <app_name1> [app_name2] [app_name3] ...")
        return

    app_names = sys.argv[1:]

    yabai_windows, ret_code = run_bash_command("yabai -m query --windows", json_output=True)

    if ret_code != 0 or yabai_windows is None:
        return

    for app_name in app_names:
        window = get_window_data_from_application_name(yabai_windows, app_name)

        # If the window was found, focus to it and exit
        if window is not None:
            run_bash_command(f"yabai -m space --focus {window['space']}")
            run_bash_command(f"yabai -m window --focus {window['id']}")
            print(f"Focused on {app_name}")
            return

    print("None of the specified applications were found.")


if __name__ == "__main__":
    main()
