import os
import pickle

from file_paths import NOTE_DATA
from file_paths import BACKUP_DATA


def save_data(data, backup=False):
    """
    data = {
        'test_note': {
            'description': ': description',
            'tags': ['tag'],
            'timestamp': 'now'}
        }
    }

    :param data: (dict) containing all notes.
    :param backup: (boolean) save data to backup.
    """
    if backup == False:
        with open(NOTE_DATA, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(BACKUP_DATA, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def load_data():
    """ Load the note data into a dict."""
    try:
        with open(NOTE_DATA, 'rb') as _input:
            return pickle.load(_input)

    except EOFError and IOError:
        return {}

