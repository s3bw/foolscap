import os

from foolscap.file_paths import NOTE_FOLDERS
from foolscap.handle_note_io import (
    load_text,
    edit_text,
    unique_text,
)

from foolscap.meta_data import (
    shift_lines,
    note_exists,
    new_component,
    remove_component,
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
        print("\n\tSaved note: '{}'.\n".format(titles[0]))
    else:
        for title, content in zip(titles, contents):
            print("\n\tAdded: '{}'.\n".format(title))


def export_note(note):
    if note_exists(note):
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
        delete_file = folders['GET_NOTE'].format(note_name=note)

        recycle_bin = unique_text(note, folder='IN_BIN')
        bin_note = folders['BIN_NOTE'].format(note_name=recycle_bin)

        os.rename(delete_file, bin_note)
        remove_component(note)
        print("\n\tDeleted: '{}'.\n".format(note))


def edit_note(note):
    """ Edit the note from data in vim.

    :param note: (string) name of .txt file.
    :param stored_data: (dict) of notes in data.
    """
    if note_exists(note):
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        edit_text(editing=edited_note)

        update_component(note)
        print("\n\tUpdated: '{}'.\n".format(note))


def new_note():
    """ Create a new note in vim from template.

    :param stored_notes: (dict) of notes in data.
    """
    new_text = edit_text()
    # don't write unchanged notes.
    if '# title' == new_text[0]:
        print('\n\tAborted Note.\n')
    else:
        save_note(new_text, temp_file=True)


def move_lines(from_note):
    """ Move selected lines from a note to another note.

    :param note: (string) title of note to move lines to.
    :param stored_data: (dict) of notes in data.
    """
    note = input('Move lines to? ')

    if note_exists(note) and note_exists(from_note):
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=from_note)
        edit_text(editing=edited_note)

        shift_lines(from_note, note)


