import sys
import argparse

from note_data import note_data
from note_content import (
    save_note,
    view_note,
    list_notes,
    delete_note,
    edit_note,
    new_note,
    move_lines,
)


FUNCTION_MAP = {
    'save': save_note,
    '-s': save_note,
    'view': view_note,
    '-v': view_note,
    'list': list_notes,
    '-ls': list_notes,
    'delete': delete_note,
    '-d': delete_note,
    'edit': edit_note,
    '-e': edit_note,
    'new': new_note,
    '-n': new_note,
    'move_lines': move_lines,
    '-ml': move_lines,
}

parser = argparse.ArgumentParser()
parser.add_argument(
    'command',
    choices=FUNCTION_MAP.keys(),
)
parser.add_argument(
    'positional',
    action='store',
    nargs='?',
)


def main():
    args = parser.parse_args()

    command = args.command
    action = FUNCTION_MAP[command]
    note_args = args.positional
    whole_foolscap = note_data()

    if note_args:
        action(note_args, whole_foolscap)
    elif command == 'list' or command == 'ls':
        action(None, whole_foolscap)
    else:
        action(whole_foolscap)


