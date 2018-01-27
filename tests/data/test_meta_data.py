import datetime


def mock_data(views, year=2000):
    modified = modified=datetime.datetime(year, 12, 10, 15, 25, 19, 11262)
    return {
        'description': 'This is a fake note',
        'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
        'modified': modified,
        'tags': ['fake_tag'],
        'views': views
    }


FAKE_SINGLE_NOTE = {
    'most_viewed': mock_data(4)
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
