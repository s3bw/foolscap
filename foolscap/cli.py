import argparse

from foolscap.actor import action


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

LIST_TYPES = [
    'tags',
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
parser.add_argument(
    '-t',
    '--list_type',
    default='normal',
    choices=LIST_TYPES,
)


def main():
    args = parser.parse_args()
    command = args.command
    note_args = args.positional
    list_type = args.list_type

    action(command, note_args, list_type)

