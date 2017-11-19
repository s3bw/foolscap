from display.console import display_list


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
        print("No note tagged with '{tag}'".format(tag=tags))

    all_notes = [
        (k, values['description']) 
        for k, values in all_notes.items()
    ]

    display_list(all_notes)
