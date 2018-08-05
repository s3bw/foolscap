from foolscap.file_paths import NOTE_FOLDERS

from foolscap.handle_note_io import load_text
from foolscap.handle_note_io import edit_text
from foolscap.handle_note_io import move_text_to_bin

from foolscap.meta_data import (
    shift_lines,
    note_exists,
    new_component,
    remove_component,
    update_component,
    upgrade_components,
)
from foolscap.meta_data import parse_note


def update_notes():
    upgrade_components()


# Possibly two functions?
def save_note(new_note, temp_file=False):
    """ Convert note.txt to dict components and save.

    :param new_note: (string) pointing to a note.
    :param temp_file: (boolean) indicating the note
        instance needs to be added.
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
    """ Write a copy of note in current directory.
    """
    if note_exists(note):
        note_text = load_text(note)
        with open(note + '.txt', 'w') as write_file:
            for line in note_text:
                write_file.write(line + '\n')

        update_component(note)
        print("\n\tExported: '{}'.\n".format(note))


def view_note(note):
    """ Print the note to console.

    :param str note: the name of the note to print.

    Snippets of notes can be printed by prefixing start and end line
        in the following format: <note_name>@<start>:<end>
        E.g: note_name@3:6
    Otherwise the whole note will be printed when provide just the
        note name: <note_name>
    """
    note, _min, _max = parse_note.name(note)
    if note_exists(note):
        note_text = load_text(note)
        if _max == 0:
            _max = len(note_text)

        for line in note_text[_min:_max]:
            print(line)

        update_component(note)


def delete_note(note):
    """ Delete a note stored in foolscap
    """
    if note_exists(note):
        move_text_to_bin(note)
        remove_component(note)
        print("\n\tDeleted: '{}'.\n".format(note))


def edit_note(note):
    """ Edit the note in vim.
    """
    if note_exists(note):
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
        edit_text(editing=edited_note)

        update_component(note)
        print("\n\tUpdated: '{}'.\n".format(note))


def new_note():
    """ Create a new note from template.
    """
    new_text = edit_text()
    # don't write unchanged notes.
    if '# title' == new_text[0]:
        print('\n\tAborted Note.\n')
    else:
        save_note(new_text, temp_file=True)


def move_lines(from_note):
    """ Move selected lines from a note to another note.
    """
    note = input('Move lines to? ')

    if note_exists(note) and note_exists(from_note):
        edited_note = NOTE_FOLDERS['GET_NOTE'].format(note_name=from_note)
        edit_text(editing=edited_note)

        shift_lines(from_note, note)

