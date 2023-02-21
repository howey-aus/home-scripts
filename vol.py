#!/usr/bin/env python3
"""
Simplified interface for controlling `amixer` audio levels.

Usage:
    script.py <capability> [action]

Parameters:
    capability:
        - p: Playback
        - c: Capture
    action (optional):
        - +:   Increase volume by 5%
        - -:   Decrease volume by 5%
        - =:   Set volume to 0%
        - t:   Toggle mute/unmute
        - i3b: Increase or decrease volume depending on value of BLOCK_BUTTON environment variable

Example:
    script.py p +  # Increases playback volume by 5%

    (when invoked from i3blocks) script.py p i3b
"""

import sys
import os
import subprocess
import re

CAPABILITIES = {
    'p': ('Master', 'Playback'),
    'c': ('Capture', 'Capture'),
}

ACTIONS = {
    '+': '5%+',
    '-': '5%-',
    '=': '0%-',
    't': 'toggle',
}

# Handle i3blocks click events if applicable
if block_button := os.environ.get('BLOCK_BUTTON'):
    ACTIONS['i3b'] = {
        '4': ACTIONS['+'],
        '5': ACTIONS['-'],
    }.get(block_button, ACTIONS['='])


def parse_amixer_output(output, cap_req):
    capability = 'Playback' if cap_req != 'c' else 'Capture'
    pattern = fr"Front Left: {capability} \d+ \[(\d+%)\] \[(\w+)\]"
    match = re.search(pattern, output)
    return match.groups()


def main():
    try:
        capability_req = sys.argv[1]
    except IndexError:
        capability_req = '--help'

    if capability_req in ['--help', '-h']:
        print(__doc__)
        exit(0)

    action_req = sys.argv[2] if len(sys.argv) > 2 else '='

    capability = CAPABILITIES.get(capability_req, CAPABILITIES['p'])
    action = ACTIONS.get(action_req, ACTIONS['='])
    command = ['amixer', '-M', 'sset', *capability, action]

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        stdout, _ = proc.communicate()
        level_status, on_status = parse_amixer_output(stdout, capability_req)

    print(level_status if on_status == 'on' else '--')

    # Send signal to i3blocks if this was invoked by anything other than i3blocks.
    if action_req != 'i3b':
        subprocess.run(['pkill', '-RTMIN+1', 'i3blocks'])


if __name__ == '__main__':
    main()
