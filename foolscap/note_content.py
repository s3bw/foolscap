import os

from foolscap.file_paths import NOTE_FOLDERS
from foolscap.handle_note_io import (
    load_text,
    edit_text,
    save_text,
    remove_text,
    unique_text,
)

from foolscap.meta_data import (
    note_exists,
    new_component,
    update_component,
    upgrade_components,
)

def update_notes():
    upgrade_components()


def save_note(new_note, temp_file=False):
    """ Convert note.txt to dict components and save.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    # Used for parsing '.txt' notes.
    if not temp_file:
        new_note = load_text(new_note, new_note=True)
    titles, contents = new_component(new_note)
    if temp_file:
        # save_text(note_titles[0], contents[0])
        print("\n\tSaved note: '{}'.\n".format(titles[0]))
    else:
        for title, content in zip(titles, contents):
            # save_text(title, content)
            print("\n\tAdded: '{}'.\n".format(title))


def export_note(note):
    if note_exists:
        note_text = load_text(note)
        with open(note + '.txt', 'w') as write_file:
            for line in note_text:
                write_file.write(line + '\n')

        update_component(note)
        print("\n\tExported: '{}'.\n".format(note))


def view_note(note):
    """ Print the note to console if found.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    if note_exists(note):
        # Move to IO handler:
        note_text = load_text(note)
        for line in note_text:
            print(line)

        update_component(note)


def delete_note(note):
    """ Delete a note stored in foolscap

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    if note_exists(note):
        folders = NOTE_FOLDERS
        # IO Hander
        delete_file = folders['GET_NOTE'].format(note_name=note)

        # Move unique heading to components
        recycle_bin = unique_text(note, folder='IN_BIN')
        bin_note = folders['BIN_NOTE'].format(note_name=recycle_bin)

        os.rename(delete_file, bin_note)
        print("\n\tDeleted: '{}'.\n".format(note))


def edit_note(note):
    """ Edit the note from data in vim.

    :param note: (string) name of .txt file.
    :param stored_data: (dict) of notes in data.
    """
    if note_exists(note):
        # path to Handle IO
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        edit_text(editing=edited_note)

        update_component(note)
        print("\n\tUpdated: '{}'.\n".format(note))


def new_note():
    """ Create a new note in vim from template.

    :param stored_notes: (dict) of notes in data.
    """
    # Edit text to Handle IO
    new_text = edit_text()
    # don't write unchanged notes.
    if '# title' == new_text[0]:
        print('\n\tAborted Note.\n')
    else:
        save_note(new_text, temp_file=True)


def move_lines(note):
    """ Move selected lines from a note to another note.

    :param note: (string) title of note to move lines to.
    :param stored_data: (dict) of notes in data.
    """
    from_note = input('Move lines from? ')

    if note_exists(note) and note_exists(from_note):
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=from_note)
        edit_text(editing=edited_note)

        shift_lines(from_note, note)


def remove_moving_lines(note):
    _lines = [line for line in note if line[:1] != '>']
    return _lines


def shift_lines(name_from_note, name_to_note):
    # load text, return note, delete, save new
    take_from_note = load_text(path_from)
    remove_text(path_from)

    replace_note = get_contents(take_from_note)[0]
    replace_note = remove_moving_lines(replace_note)
    save_text(name_from_note, replace_note)

    # load text, return note, apply new, delete old, save new
    apply_to_note = load_text(name_to_note)
    # Get contents with be tricky to refactor
    apply_to_note = get_contents(apply_to_note)[0]

    line_index = len(apply_to_note) - 2
    # Insert moved lines into other note.
    apply_to_note[line_index:line_index] = get_moving_lines(take_from_note)
    remove_text(name_to_note)
    save_text(name_to_note, apply_to_note)


