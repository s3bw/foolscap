from datetime import datetime

from foolscap.handle_note_io import save_text
from foolscap.handle_note_io import load_text
from foolscap.handle_note_io import replace_text
from foolscap.handle_note_io import unique_text

from foolscap.meta_data.io import load_meta
from foolscap.meta_data.io import save_meta
from foolscap.meta_data.io import migrate_meta
from foolscap.meta_data.utils import fuzzy_guess
from foolscap.meta_data.transformations import load_tags

from foolscap.meta_data.parse_note import (
    restrict_title,
    get_title,
    get_contents,
    get_moving_lines,
    note_tags,
    note_description,
    parse_sub_headings,
)


def upgrade_components():
    migrate_meta()


def tag_exists(tag):
    stored_tags = load_tags()
    if tag in stored_tags:
        return True
    else:
        fuzzy_guess(tag, stored_tags)


def note_exists(note):
    stored_notes = load_meta().keys()
    if note in stored_notes:
        return True
    else:
        fuzzy_guess(note, stored_notes)


def remove_moving_lines(note):
    _lines = [line for line in note if line[:1] != '>']
    return _lines


def shift_lines(path_from, name_to_note):
    # load text, return note, delete, save new
    from_note = load_text(path_from)

    replace_note = get_contents(from_note)[0]
    replace_note = remove_moving_lines(replace_note)
    replace_text(path_from, path_from, replace_note)

    # load text, return note, apply new, delete old, save new
    apply_to_note = load_text(name_to_note)
    # Get contents with be tricky to refactor
    apply_to_note = get_contents(apply_to_note)[0]

    line_index = len(apply_to_note) - 2
    # Insert moved lines into other note.
    apply_to_note[line_index:line_index] = get_moving_lines(from_note)
    replace_text(name_to_note, name_to_note, apply_to_note)


def remove_component(note):
    stored_notes = load_meta()
    stored_notes.pop(note, None)
    save_meta(stored_notes)


def add_component(component):
    stored_notes = load_meta()
    stored_notes.update(component)
    save_meta(stored_notes)


def avoid_conflict(note, new_name, stored_data):
    """ Check if note name has changed and that the new name
    does not exists in the note directory.
        - if there is a conflict, find a name that does not
          conflict
    """
    stored_notes = stored_data.keys()
    if new_name != note and new_name in stored_notes:
        print('Warning!: Edited note title already exists!')
        new_name = unique_text(new_name)
    return new_name


def update_note_hooks(note, stored_data):
    """ If the name of note has been changed, update the
    hook in the meta_data (hash key).
    """
    note_edited = load_text(note)
    new_name = restrict_title(get_title(note_edited)[0])
    new_content = get_contents(note_edited)[0]
    new_name = avoid_conflict(note, new_name, stored_data)

    # Note name has been changed, update the meta_data hook.
    if new_name != note:
        stored_data[new_name] = stored_data[note]
        stored_data.pop(note, None)

    replace_text(note, new_name, new_content)
    return new_name, new_content


def update_component(note):
    stored_data = load_meta()

    new_name, content = update_note_hooks(note, stored_data)

    stored_data[new_name]['modified'] = datetime.now()
    stored_data[new_name]['views'] += 1

    description = note_description(content)
    if description:
        stored_data[new_name]['description'] = description

    tags = note_tags(content)
    if tags:
        stored_data[new_name]['tags'] = tags

    sub_headings = parse_sub_headings(content)
    if sub_headings:
        stored_data[new_name]['sub_headings'] = sub_headings
        stored_data[new_name]['num_sub'] = len(sub_headings)

    save_meta(stored_data)


def new_component(text):
    """ Creates the new note data structure.
        Here is where one would add more note information.

    :param list[str] note: containing a single note.
    :return: the dict note element.
    """
    # Text should be a string.
    # Passing to parse text should return basic components.
    # This function should then append components not found in note
    titles = get_title(text)
    contents = get_contents(text)

    # This loops through multiple notes
    note_component = {}
    for note_title, content in zip(titles, contents):
        note_title = restrict_title(note_title)
        title = unique_text(note_title)

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
            note_component[title]['num_sub'] = len(sub_headings)

    add_component(note_component)
    return titles, contents
