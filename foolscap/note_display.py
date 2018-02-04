from foolscap.display.console import display_list
from foolscap.meta_data import load_meta

TOP_X_VIEWED = 3
# This rule is so perfectly subtle,
# - the number of views on notes
# - is so few at this stage
# - that one doesn't even notice it take effect.
SORT_BY_VIEWS_RULE = 5


def list_notes(tags):
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
    all_notes = load_meta()
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


def most_viewed(note_dict):
    """ Remove top notes from dict

    Unless less than sort_by_views_rule:
        - don't rank most viewed to index 2, 3, 4 if
          notes number less than 5.
    """
    organised_notes = []
    num_notes = len(list(note_dict))
    if num_notes > SORT_BY_VIEWS_RULE:
        organised_notes = pull_top_viewed(note_dict)
        for note in organised_notes:
            note_dict.pop(note)
    return organised_notes


def pull_top_viewed(note_dict):
    """ Get top X viewed notes.
    """
    note_and_views = [
        (note_title, note_dict[note_title]['views'])
        for note_title in note_dict
    ]
    # Sort by views then sort by name.
    sorted_by_views = sorted(note_and_views, key=lambda x: (-x[1], x[0]))
    return [
        note_name
        for note_name, _ in sorted_by_views[:TOP_X_VIEWED]
    ]


def sort_notes(note_data):
    """ Custom sort to display notes.

    - Last Opened (unless in top 3 most viewed)
    - 1st Most Views
    - 2nd Most Views
    - 3rd Most Views
    - A to Z
    """
    data_copy = note_data.copy()

    organised_notes = most_viewed(data_copy)

    # Own function
    last_opened = find_last_opened(data_copy)
    if last_opened:
        organised_notes.insert(0, last_opened)
        data_copy.pop(last_opened)

    remaining_notes = list(data_copy)
    alphabetise = sorted(remaining_notes, key=lambda x: x.lower())

    return [
        note_title
        for note_title in organised_notes + alphabetise
        if note_title is not None
    ]

