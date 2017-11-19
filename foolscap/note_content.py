import os

from meta_data import save_data
from parse_text import (
    load_text,
    edit_text,
    unique_heading,
    shift_lines,
    note_component,
    update_component,
)
from file_paths import NOTE_FOLDERS


def save_note(new_note, saved_notes, temp_file=False):
    """ Convert note.txt to dict components and save.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """

    if not temp_file:
        new_note = load_text(new_note)

    new_component = note_component(new_note)

    saved_notes.update(new_component)
    save_data(saved_notes)


def view_note(note, stored_data):
    """ Print the note to console if found.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    name_note = NOTE_FOLDERS['GET_NOTE']

    if note in stored_notes:
        note_text = load_text(name_note.format(note_name=note))

        for line in note_text:
            print(line)

    else:
        # Fuzzy here
        print('Not found')


def delete_note(note, stored_data):
    """ Delete a note stored in foolscap

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()

    if note in stored_notes:
        folders = NOTE_FOLDERS

        delete_file = folders['GET_NOTE'].format(note_name=note)

        recycle_bin = unique_heading(note, folder='IN_BIN')
        bin_note = folders['BIN_NOTE'].format(note_name=recycle_bin)

        os.rename(delete_file, bin_note)

        stored_data.pop(note, None)
        save_data(stored_data)

    else:
        # Fuzzy here
        print('Not found')


def edit_note(note, stored_data):
    """ Edit the note from data in vim.

    :param note: (string) name of .txt file.
    :param stored_data: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()

    if note in stored_notes:
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        edit_text(editing=edited_note)

        stored_data = update_component(note, stored_data)
        save_data(stored_data)

        print('Note updated')

    else:
        # Fuzzy here
        print('Not found')


def new_note(stored_notes):
    """ Create a new note in vim from template.

    :param stored_notes: (dict) of notes in data.
    """
    new_text = edit_text()

    # don't write unchanged notes.
    if '# title' != new_text[0]:
        save_note(new_text, stored_notes, temp_file=True)

    else:
        print('Aborted New Note')


def move_lines(note, stored_data):
    """ Move selected lines from a note to another note.

    :parma note: (string) title of note to move lines to.
    :param stored_data: (dict) of notes in data.
    """
    from_note = input('Move lines from? ')

    stored_notes = stored_data.keys()
    if note not in stored_notes:
        print('{} not found.'.format(note))

    if from_note in stored_notes:
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=from_note)
        edit_text(editing=edited_note)

        stored_data = shift_lines(from_note, note)
    else:
        print('{} not found.'.format(from_note))

