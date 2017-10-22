import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

NOTE_DIR = '\\notes\\'
REAL_DIR = SCRIPT_DIR + NOTE_DIR

NOTE_STORAGE = '\\notes\\{note_name}.txt'
REAL_NOTE = SCRIPT_DIR + NOTE_STORAGE


def load_text(text):
    with open(text) as notes:
        notes = notes.read()
        return notes.split('\n')


def unique_note(heading):
    saved_notes = [filename for filename in os.listdir(REAL_DIR)]

    suffix = 0
    if '{heading}.txt'.format(heading=heading) in saved_notes:
        while '{}_{}.txt'.format(heading, str(suffix)) in saved_notes:
            suffix += 1

        new_name = '{}_{}'.format(heading, str(suffix))
        heading = new_name

    return heading


def save_text(heading, content):
    """ This saves the note as a text file.

    :param heading: (string) the heading of the note used as filename.
    :param content: (list) containing the lines of the note.
    """
    heading = unique_note(heading)

    text_string = '\n# {heading}\n'.format(heading=heading)
    text_string += '\n'.join(content)

    name_note = REAL_NOTE.format(
        note_name=heading
    )

    with open(name_note, 'w') as save_txt:
        save_txt.write(text_string)

    return heading


def get_sections(note):
    # Section parsing needs improvement
    _sections = [line[2:] for line in note if line[:2] == '# ']
    return _sections


def get_moving_lines(note):
    _lines = [line for line in note if line[:1] == '>']
    return _lines


def remove_moving_lines(note):
    _lines = [line for line in note if line[:1] != '>']
    return _lines


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def note_description(content):
    # Needs to return multiple descriptions (sectioning)
    description = content[1]
    if description and description[0] == ':':
        return description
    return None


def note_tags(contents):
    tag_line = contents[-2]

    if tag_line and '{' in tag_line:
        tags = [tag[1:-1] for tag in tag_line.split(' ') if tag]
        return tags
    return None


def get_contents(note):
    content_index = [
        index
        for index, line
        in enumerate(note)
        if line[:2] == '=='
    ]

    content_list = []
    indexes = pairwise(content_index)

    for start, end in indexes:
        content = note[start:end+1]
        content_list.append(content)

    return content_list


def note_component(note_lines):
    """ Creates the new note data structure.
        Here is where one would add more note information.

    :param note: (list) of string containing a single note.
    :return: the dict note element.
    """
    sections = get_sections(note_lines)
    contents = get_contents(note_lines)

    note_component = {}
    for heading, content in zip(sections, contents):
        heading = save_text(heading, content)

        note_component[heading] = {
            'timestamp': None,
        }

        note_component[heading]['timestamp'] = 'now'

        description = note_description(content)
        if description:
            note_component[heading]['description'] = description

        tags = note_tags(content)
        if tags:
            note_component[heading]['tags'] = tags

    return note_component


def shift_lines(from_note, note):
    path_from = REAL_NOTE.format(note_name=from_note)
    _from = load_text(path_from)

    move_lines = get_moving_lines(_from)

    new_from = get_contents(_from)[0]

    new_from = remove_moving_lines(new_from)

    os.remove(path_from)
    save_text(from_note, new_from)

    path_to = REAL_NOTE.format(note_name=note)
    _to = load_text(path_to)
    _to = get_contents(_to)[0]

    new_line_index = len(_to) - 2

    # Insert new lines into 'to' note.
    _to[new_line_index:new_line_index] = move_lines

    os.remove(path_to)
    save_text(note, _to)


def update_component(note, stored_data):
    stored_notes = stored_data.keys()

    note_name = REAL_NOTE.format(
        note_name=note
    )
    note_edited = load_text(note_name)

    new_name = get_sections(note_edited)[0]
    new_content = get_contents(note_edited)[0]

    if new_name != note and new_name in stored_notes:
        print('Warning!: Edited note title already exists!')
        new_name = unique_note(new_name)

    if new_name != note and new_name not in stored_notes:
        stored_data[new_name] = stored_data[note]
        stored_data.pop(note, None)

    os.remove(note_name)
    save_text(new_name, new_content)

    stored_data[new_name]['updated'] = 'at_this_time'

    # stored_data[new_name]['times_viewed'] += 1

    description = note_description(new_content)
    if description:
        stored_data[new_name]['description'] = description

    tags = note_tags(new_content)
    if tags:
        stored_data[new_name]['tags'] = tags

    return stored_data

