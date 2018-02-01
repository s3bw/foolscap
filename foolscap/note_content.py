import os

from file_paths import NOTE_FOLDERS # io handler
from parse_text import (
    load_text, # IO handler
    edit_text # IO handler,
    unique_heading, # new component?
    shift_lines, # move here
)
from meta_data import (
    new_component,
    update_component,
)


def save_note(new_note, temp_file=False):
    """ Convert note.txt to dict components and save.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    # Used for parsing '.txt' notes.
    if not temp_file:
        new_note = load_text(new_note)
    titles, contents  = new_component(new_note)
    if temp_file:
        title = note_titles[0]
        content = contents[0]
        save_text(title, content)
        print("\n\tSaved note: '{}'.\n".format(title))
    else:
        for title, content in zip(titles, contents):
            save_text(title, content)
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
        recycle_bin = unique_heading(note, folder='IN_BIN')
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

