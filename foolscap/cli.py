import argparse

from meta_data import note_data
from note_display import list_notes
from note_content import (
    save_note,
    view_note,
    delete_note,
    edit_note,
    new_note,
    move_lines,
)

# map <> {'-s': 'save'}
FUNCTION_MAP = {
    'save': save_note,
    'view': view_note,
    'list': list_notes,
    'delete': delete_note,
    'edit': edit_note,
    'new': new_note,
    'move_lines': move_lines,
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
    elif command == 'list':
        action(None, whole_foolscap)
    else:
        action(whole_foolscap)

