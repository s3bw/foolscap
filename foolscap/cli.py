import argparse

from meta_data import load_data
from actor import action


FEATURES = [
    'save',
    'view',
    'list',
    'delete',
    'edit',
    'new',
    'move_lines',
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

