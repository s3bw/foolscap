import datetime


FAKE_SINGLE_NOTE = {
    'most_viewed':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 4
        }
}


FAKE_MANY_NOTES = {
    'most_viewed':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 4
        },
    'A':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 1
        },
    'recently_opened':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2018, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 1
        },
    'second_most':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 3
        },
    'third_most':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 2
        },
    'fake_note_1':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 1
        },
    'Z':
        {
            'description': 'This is a fake note',
            'created': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'modified': datetime.datetime(2000, 12, 10, 15, 25, 19, 11262),
            'tags': ['fake_tag'],
            'views': 1
        }
    }
