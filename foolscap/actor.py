import sys
from socket import socket
from socket import AF_UNIX
from socket import SOCK_DGRAM

from foolscap.note_display import Controller
from foolscap.note_content import (
    save_note,
    view_note,
    delete_note,
    edit_note,
    new_note,
    export_note,
    move_lines,
    update_notes,
)

# map <> {'-s': 'save'}
FUNCTION_MAP = {
    'save': save_note,
    'view': view_note,
    'delete': delete_note,
    'edit': edit_note,
    'new': new_note,
    'export': export_note,
    'move_lines': move_lines,
    'migrate': update_notes,
    'list': None,
    'search': None,
}

DISPLAY_ACTIONS = [
    'list',
    'search',
]


def grab_attention(process_name):
    """ Binds foolscap to an abstract port on Linux, will
        interrupt foolscap if it tries to bind to the port
        whilst another instance of foolscap is active.
    """
    grab_attention._lock = socket(AF_UNIX, SOCK_DGRAM)
    try:
        grab_attention._lock.bind("\0" + process_name)
    except OSError:
        print("\n\tFoolscap is operating elsewhere!\n")
        sys.exit()


def action(do_action, arg, list_type='notes', book='general'):
    if sys.platform.startswith("linux"):
        # Linux specific abstract namespace domain socket
        grab_attention("foolscap_actor")

    func = FUNCTION_MAP[do_action]

    new_action = {}
    if do_action in DISPLAY_ACTIONS:
        display_ctrl = Controller(list_type)

        # Quitting from list calls exit() method.
        # arg is filter in this case
        if arg:
            if do_action == 'search':
                new_action = display_ctrl.search_output(arg)
            else:
                new_action = display_ctrl.query_output(arg)
        else:
            new_action = display_ctrl.basic_output(book)

    if new_action and (new_action.action not in ['close', 'exit']):
        if new_action.action in ['next', 'prev']:
            new_func = 'list'
            action(new_func, None, book=new_action.key)
        elif new_action.action == 'select':
            new_func = 'edit'
            note = new_action.key
            action(new_func, note)
    # arg is note in this case
    elif arg:
        func(arg)
    else:
        func()
