from datetime import datetime

import pytest
from mock import patch
from mock import call

from foolscap.meta_data.io import migrate_meta

from tests.data.mock_meta_data import mock_w_subheadings


FAKE_TIME = datetime(2000, 12, 10, 15, 25, 19, 11262)
FAKE_DATA = {
    'test_note': {
        'description': 'This is a fake note',
        'tags': ['fake_tag'],

        # Gets indexes
        'sub_headings': [('First Sub:', ':A sub headings')],

        # Gets popped
        'timestamp': 'now',
        'updated': 'now',
    },
    'test_note_1': {
        'description': 'This is a fake note',
        'tags': ['fake_tag'],
        'sub_headings': [('First Sub:', ':A sub headings')],
        'create': FAKE_TIME,

    },
    'test_note_2': {
        'description': 'This is a fake note',
        'tags': ['fake_tag'],
        'sub_headings': [('First Sub:', ':A sub headings', 1, 1)],
        'created': FAKE_TIME,
        'create': 'no time',
    }
}


def test_migrate_meta_old_to_new():
    patch_load = 'foolscap.meta_data.io.load_meta'
    patch_save = 'foolscap.meta_data.io.save_meta'
    patch_time = 'foolscap.meta_data.io.datetime'

    with patch(patch_load, return_value=FAKE_DATA),\
         patch(patch_save) as save_mock,\
         patch(patch_time) as time_mock:

        time_mock.now.return_value = FAKE_TIME

        # Both Calls end up being the same due to mutating the dict
        expected_data = {
            'test_note': mock_w_subheadings(1),
            'test_note_1': mock_w_subheadings(1),
            'test_note_2': mock_w_subheadings(1),
        }

        expected_calls = [
            call(expected_data, backup=True),
            call(expected_data)
        ]

        migrate_meta()
        save_mock.assert_has_calls(expected_calls)

