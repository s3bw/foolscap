from foolscap.note_display import list_notes
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
    'list': list_notes,
    'delete': delete_note,
    'edit': edit_note,
    'new': new_note,
    'export': export_note,
    'move_lines': move_lines,
    'migrate': update_notes,
}


def action(do_action, arg):
    func = FUNCTION_MAP[do_action]

    new_action = None
    if do_action == 'list':
        # Quitting from list calls exit() method.
        # arg is filter in this case
        if arg:
            new_action = func(arg)
        else:
            new_action = func(None)

    if new_action:
        new_func, note = new_action
        action(new_func, note)
    # arg is note in this case
    elif arg:
        func(arg)
    else:
        func()

