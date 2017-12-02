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


def action(do_action, meta_data, *args):
    func = FUNCTION_MAP[do_action]

    new_action = None
    if do_action == 'list':
        if args[0]:
            filter_tag = args[0]
            new_action = func(filter_tag, meta_data)
        else:
            new_action = func(None, meta_data)
    if new_action:
        new_func, note = new_action
        action(new_func, meta_data, note)
    elif args:
        note = args[0]
        func(note, meta_data)
    else:
        func(meta_data)
        
