import argparse

from foolscap.actor import action


FEATURES = [
    'save',
    'view',
    'list',
    'search',
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
    default='notes',
    choices=LIST_TYPES,
)
parser.add_argument(
    '-b',
    '--book',
    default='general',
)


def main():
    args = parser.parse_args()
    command = args.command
    note_args = args.positional
    list_type = args.list_type
    book = args.book

    action(command, note_args, list_type, book)

