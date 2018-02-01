import os
from tempfile import NamedTemporaryFile

from file_paths import NOTE_FOLDERS
from subprocess_utils import edit_in_vim


NEW_NOTE_TEMPLATE = """\
# title
==========
: description
Make sure you change the title!


{tag}
=========="""

def remove_text(note):
    path = NOTE_FOLDERS['GET_NOTE'].format(note_name=name_to_note)
    os.remove(path)

def load_text(note):
    path = NOTE_FOLDERS['GET_NOTE'].format(note_name=name_to_note)
    with open(text) as notes:
        notes = notes.read()
        # Handle for dos and unix
        return notes.split('\n')


def edit_text(editing=None):
    # Maybe this can be split into two functions in subprocess_utils
    if not editing:
        with NamedTemporaryFile(mode='r+', suffix='.tmp') as editing_text:
            editing_text.write(NEW_NOTE_TEMPLATE)
            edit_in_vim(editing_text)
            editing_text.seek(0)
            return editing_text.read().split('\n')
    with open(editing, 'r') as editing_text:
        edit_in_vim(editing_text)


def save_text(note_title, content):
    """ This saves the note as a text file.
    :param str note_title: the title of the note used as filename.
    :param list[str] content: containing the lines of the note.
    """
    text_string = '\n# {heading}\n'.format(heading=note_title)
    text_string += '\n'.join(content)
    name_note = NOTE_FOLDERS['GET_NOTE'].format(
        note_name=note_title
    )
    with open(name_note, 'w') as save_txt:
        save_txt.write(text_string)


