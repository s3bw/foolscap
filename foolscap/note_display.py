from display.console import display_list


TOP_X_VIEWED = 3


def list_notes(tags, all_notes):
    """ Presents notes in the terminal.

    all_notes = {
        'note_title: {
            'description': 'note description',
            'timestamp': 'TIME',
            'updated': 'TIME',
            'tags': ['tag', 'example'],
        }
    }

    :param str tags: Filter by tag.
    :param dict[dict[list]] all_notes: Meta information on notes.
    """
    if tags:
        all_notes = {
            key: values
            for key, values in all_notes.items()
            if 'tags' in values and tags in values['tags']
        }

    if len(all_notes) == 0:
        # Fuzzy here
        print("No note tagged with '{tag}'".format(tag=tags))
        exit()

    sorted_titles = sort_notes(all_notes)
    display_notes = display_information(sorted_titles, all_notes)

    return display_list(display_notes)


def display_information(sorted_notes, note_dict):
    """ Get description from list of note titles"""
    return [
        (title, note_dict[title]['description'])
        for title in sorted_notes
    ]


def modified_notes(note_dict):
    """Notes that have been modified"""
    return [
        (key, values['modified'])
        for key, values in note_dict.items()
        if 'modified' in values
    ]


def find_last_opened(note_data):
    """Most recently modified"""
    modified = modified_notes(note_data)
    # All cases should have modified.
    # Remove once Issue #56. is resolved.
    if modified:
        return max(modified, key=lambda x: x[1])[0]


def most_views_pop(note_dict):
    """ Get most viewed note and remove it from dict.
    """
    if note_dict:
        max_views = max(note_dict, key=lambda x: note_dict[x]['views'])
        note_dict.pop(max_views)
        return max_views


def sort_notes(note_data):
    """ Custom sort to display notes.

    - Last Opened (unless in top 3 most viewed)
    - 1st Most Views
    - 2nd Most Views
    - 3rd Most Views
    - A to Z
    """
    data_copy = note_data.copy()

    # I could iter this instead of looping
    # sort list, grab first 3.
    organised_notes = []
    for _ in range(TOP_X_VIEWED):
        organised_notes.append(most_views_pop(data_copy))

    last_opened = find_last_opened(data_copy)
    if last_opened:
        organised_notes.insert(0, last_opened)
        data_copy.pop(last_opened)

    alphabetise = sorted(list(data_copy), key=lambda x: x.lower())

    return [
        note_title
        for note_title in organised_notes + alphabetise
        if note_title is not None
    ]

