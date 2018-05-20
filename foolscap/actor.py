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


def action(do_action, arg, list_type='notes'):
    func = FUNCTION_MAP[do_action]

    new_action = None
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
            new_action = display_ctrl.basic_output()

        if not new_action:
            exit()

    print(new_action)
    if new_action:
        new_func, note = new_action
        action(new_func, note)
    # arg is note in this case
    elif arg:
        func(arg)
    else:
        func()

