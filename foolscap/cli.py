import argparse

from actor import action
from meta_data import load_data


FEATURES = [
    'save',
    'view',
    'list',
    'delete',
    'edit',
    'new',
    'export',
    'move_lines',
    'migrate',
]

parser = argparse.ArgumentParser()
parser.add_argument(
    'command',
    choices=FEATURES,
)
parser.add_argument(
    'positional',
    action='store',
    nargs='?',
)


def main():
    args = parser.parse_args()
    command = args.command
    note_args = args.positional

    whole_foolscap = load_data()
    action(command, whole_foolscap, note_args)

