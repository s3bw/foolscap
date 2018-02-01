import argparse

from actor import action


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

    action(command, note_args)

