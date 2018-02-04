import os
from tempfile import NamedTemporaryFile

from foolscap.file_paths import NOTE_FOLDERS
from foolscap.subprocess_utils import edit_in_vim


NEW_NOTE_TEMPLATE = """\
# title
==========
: description
Make sure you change the title!


{tag}
=========="""


def remove_text(note):
    path = NOTE_FOLDERS['GET_NOTE'].format(note_name=note)
    os.remove(path)


def load_text(path, new_note=False):
    if not new_note:
        path = NOTE_FOLDERS['GET_NOTE'].format(note_name=path)
    with open(path) as notes:
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


def replace_text(note, new_name, content):
    remove_text(note)
    save_text(new_name, content)


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


def unique_text(heading, folder='ALL_NOTES'):
    check_directory = NOTE_FOLDERS[folder]

    all_notes = [filename for filename in os.listdir(check_directory)]
    suffix = 0
    if '{heading}.txt'.format(heading=heading) in all_notes:
        while '{}_{}.txt'.format(heading, str(suffix)) in all_notes:
            suffix += 1
        new_name = '{}_{}'.format(heading, str(suffix))
        heading = new_name

    return heading

