import os
from datetime import datetime
from tempfile import NamedTemporaryFile

from file_paths import NOTE_FOLDERS
from subprocess_utils import edit_in_vim


MAX_TITLE_LEN = 32
NEW_NOTE_TEMPLATE = """\
# title
==========
: description
Make sure you change the title!


{tag}
=========="""


def load_text(text):
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


def unique_heading(heading, folder='ALL_NOTES'):
    check_directory = NOTE_FOLDERS[folder]

    all_notes = [filename for filename in os.listdir(check_directory)]

    suffix = 0
    if '{heading}.txt'.format(heading=heading) in all_notes:
        while '{}_{}.txt'.format(heading, str(suffix)) in all_notes:
            suffix += 1

        new_name = '{}_{}'.format(heading, str(suffix))
        heading = new_name

    return heading


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


def replace_spaces(title):
    """ Replaces spaces contained in a title."""
    if ' ' in title:
        return title.replace(' ', '_')
    return title


def max_title_len(title):
    if len(title) > MAX_TITLE_LEN:
        print('Title must be less than {} characters.'.format(MAX_TITLE_LEN))
        return title[:MAX_TITLE_LEN]
    return title


def restrict_title(title):
    return replace_spaces(max_title_len(title))


def get_title(note):
    # title parsing needs improvement (regex)
    return [restrict_title(line[2:]) for line in note if line[:2] == '# ']


def get_moving_lines(note):
    _lines = [line for line in note if line[:1] == '>']
    return _lines


def remove_moving_lines(note):
    _lines = [line for line in note if line[:1] != '>']
    return _lines


def pairwise(iterable):
    """ Pairs even length iterables.

    Returns:
        (:obj:list[tuple]) paired tuples

    Example:
        >>> pairwise([1, 2, 3, 4])
        [(1, 2), (3, 4)]
    """
    # Do I throw error for odd length iterable?
    a = iter(iterable)
    return zip(a, a)


def note_description(content):
    # Needs to return multiple descriptions (sectioning)
    description = content[1]
    if description and description[0] == ':':
        return description[1:].lstrip()
    return None


def note_tags(contents):
    tag_line = contents[-2]

    if tag_line and '{' in tag_line:
        tags = [tag[1:-1] for tag in tag_line.split(' ') if tag]
        return tags
    return None


def get_contents(note):
    """ Get note content.

    Looks for '==' lines and extract only that which
        is between them.

    parse_text.pairwise in this case, pairs sets of content-indexes
    """
    content_index = [
        index
        for index, line
        in enumerate(note)
        if line[:2] == '=='
    ]
    # This should only deal with one Note, split notes then get content.
    indexes = pairwise(content_index)

    # for start, end in indexes:
    content = [note[start:end + 1] for start, end in indexes]

    return content


def index_sub_headings(content):
    return [index
            for index, line in enumerate(content[2:])
            if line and line[0] == ':']


def parse_sub_headings(content):
    sub_headings_indexs = index_sub_headings(content)
    return [
        (content[index + 1], content[index + 2])
        if content[index + 1]
        else ('Content line {}:'.format(index + 1), content[index + 2])
        for index in sub_headings_indexs
    ]


def note_component(note_lines):
    """ Creates the new note data structure.
        Here is where one would add more note information.

    :param list[str] note: containing a single note.
    :return: the dict note element.
    """
    titles = get_title(note_lines)
    contents = get_contents(note_lines)

    # This loops through multiple notes
    note_component = {}
    for note_title, content in zip(titles, contents):
        title = unique_heading(note_title)
        save_text(title, content)

        note_component[title] = {'created': datetime.now()}
        note_component[title]['views'] = 1
        note_component[title]['modified'] = datetime.now()

        description = note_description(content)
        if description:
            note_component[title]['description'] = description

        tags = note_tags(content)
        if tags:
            note_component[title]['tags'] = tags

        sub_headings = parse_sub_headings(content)
        if sub_headings:
            note_component[title]['sub_headings'] = sub_headings

    return note_component


def shift_lines(name_from_note, name_to_note):
    # load text, return note, delete, save new
    name_note = NOTE_FOLDERS['GET_NOTE']

    path_from = name_note.format(note_name=name_from_note)
    take_from_note = load_text(path_from)
    os.remove(path_from)

    replace_note = get_contents(take_from_note)[0]
    replace_note = remove_moving_lines(replace_note)
    save_text(name_from_note, replace_note)

    # load text, return note, apply new, delete old, save new
    path_to = name_note.format(note_name=name_to_note)
    apply_to_note = load_text(path_to)
    apply_to_note = get_contents(apply_to_note)[0]

    line_index = len(apply_to_note) - 2

    # Insert moved lines into other note.
    apply_to_note[line_index:line_index] = get_moving_lines(take_from_note)

    os.remove(path_to)
    save_text(name_to_note, apply_to_note)


def update_component(note, stored_data):
    stored_notes = stored_data.keys()

    note_name = NOTE_FOLDERS['GET_NOTE'].format(
        note_name=note
    )
    note_edited = load_text(note_name)

    new_name = get_title(note_edited)[0]
    new_content = get_contents(note_edited)[0]

    if new_name != note and new_name in stored_notes:
        print('Warning!: Edited note title already exists!')
        new_name = unique_heading(new_name)

    # Note name has been changed, update the meta_data hook.
    if new_name != note and new_name not in stored_notes:
        stored_data[new_name] = stored_data[note]
        stored_data.pop(note, None)

    os.remove(note_name)
    save_text(new_name, new_content)

    stored_data[new_name]['modified'] = datetime.now()
    stored_data[new_name]['views'] += 1

    description = note_description(new_content)
    if description:
        stored_data[new_name]['description'] = description

    tags = note_tags(new_content)
    if tags:
        stored_data[new_name]['tags'] = tags

    return stored_data

