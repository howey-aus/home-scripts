#!/usr/bin/env python3
import os
import shutil
import sys


def turn_off_backlight(backlight_path, temp_path):
    """Turn off the keyboard backlight and save its current level."""
    if os.path.isfile(backlight_path):
        shutil.copy(backlight_path, temp_path)
        with open(backlight_path, 'w') as f:
            f.write("0")


def restore_backlight(backlight_path, temp_path):
    """Restore the keyboard backlight to its saved level."""
    if os.path.isfile(temp_path):
        shutil.copyfile(temp_path, backlight_path)


COMMANDS = {
    "off": turn_off_backlight,
    "restore": restore_backlight
}


def main():
    if len(sys.argv) != 2:
        print("Usage: python kb_backlight.py [off|restore]")
        sys.exit(1)

    cache_home = os.environ.get(
        'XDG_CACHE_HOME',
        os.path.join(os.path.expanduser("~"), '.cache')
    )
    temp_path = os.path.join(cache_home, "keyboard_backlight_level")
    backlight_path = "/sys/class/leds/tpacpi::kbd_backlight/brightness"

    action = COMMANDS.get(sys.argv[1])
    if action:
        action(backlight_path, temp_path)
    else:
        print("Invalid command. Use 'off' or 'restore'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
