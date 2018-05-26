import datetime


def mock_data(views, year=2000, tag='fake_tag', book='general'):
    modified = modified=datetime.datetime(year, 12, 10, 15, 25, 19, 11262)
    return {
        'description': 'This is a fake note',
        'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
        'modified': modified,
        'tags': [tag],
        'book': book,
        'views': views
    }


def mock_w_subheadings(views, year=2000, book='general'):
    modified = modified=datetime.datetime(year, 12, 10, 15, 25, 19, 11262)
    return {
        'description': 'This is a fake note',
        'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
        'modified': modified,
        'tags': ['fake_tag'],
        'book': book,
        'views': views,
        'sub_headings': [('First Sub:', ':A sub headings', 1, 1)],
        'num_sub': 1
    }


FAKE_SINGLE_NOTE_2 = {
    'most_viewed': mock_w_subheadings(4)
}


FAKE_SINGLE_NOTE = {
    'most_viewed': mock_data(4)
}

FAKE_DIFF_BOOKS = {
    'note_01': mock_data(4, book='work'),
    'note_02': mock_data(4, book='work'),
    'note_03': mock_data(4, book='work'),
    'note_04': mock_data(4, book='work'),
    'note_05': mock_data(4, book='work'),
    'note_06': mock_data(4),
    'note_07': mock_data(4),
    'note_08': mock_data(4),
    'note_09': mock_data(4),
    'note_10': mock_data(4),
    'note_11': mock_data(4),
    'note_12': mock_data(4),
    'note_13': mock_data(4),
    'note_14': mock_data(4),
}


FAKE_MANY_NOTES = {
    'most_viewed': mock_data(4),
    'second_most': mock_data(3),
    'third_most': mock_data(2),
    'recently_opened': mock_data(1, year=2018),
    'A': mock_data(1),
    'fake_note_1': mock_data(1),
    'Z': mock_data(1),
}


FOUR_FAKE_NOTES = {
    'C': mock_data(4),
    'B': mock_data(3),
    'A': mock_data(2),
    'recently_opened': mock_data(1, year=2018),
}


FOUR_FAKE_NOTES_TAGS = {
    'C': mock_data(2, tag='one'),
    'B': mock_data(2, tag='two'),
    'A': mock_data(2, tag='three'),
    'D': mock_data(2, tag='one'),
}


FAKE_NOTES_EDGE_CASE = {
    'F': mock_data(5),
    'E': mock_data(5),
    'D': mock_data(5),
    # Recent Viewed:
    'G': mock_data(5, year=2001),
    'A': mock_data(5),
    'B': mock_data(5),
    'C': mock_data(5),
}


def mock_component(views, year=2000, modified='no_change'):
    return {
        'description': 'This is a fake note',
        'created': 'created_date',
        'modified': modified,
        'tags': ['fake_tag'],
        'book': 'general',
        'views': views
    }

def MOCK_COMPONENT(x, y, name='note'):
    return {
        name: mock_component(x, modified=y)
    }
