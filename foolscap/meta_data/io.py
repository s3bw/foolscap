import pickle
from datetime import datetime

from foolscap.file_paths import NOTE_DATA
from foolscap.file_paths import BACKUP_DATA


def save_meta(data, backup=False):
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
    if not backup:
        with open(NOTE_DATA, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    else:
        with open(BACKUP_DATA, 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def load_meta():
    """ Load the note data into a dict."""
    try:
        with open(NOTE_DATA, 'rb') as _input:
            return pickle.load(_input)

    except EOFError and IOError:
        return {}


def migrate_meta():
    """
    OLD:
    data = {
        'test_note': {
            'description':  'description',
            'tags': ['tag'],
            'timestamp': 'now'}
        }
    }

    NEW:
    data = {
        'test_note': {
            'description': 'description',
            'tags': ['tag'],
            'created': datetime(),
            'modified': datetime(),
            'views': 1,
        }
    }
    """
    time_now = datetime.now()
    meta_data = load_meta()

    # Backup data before migrating
    save_meta(meta_data, backup=True)
    for key, value in meta_data.items():
        print('Migrating: {}.'.format(key))
        # Adding new meta data

        # Typo change
        meta_fields = value.keys()
        if 'create' in meta_fields and 'created' in meta_fields:
            value.pop('create', None)
        elif 'create' in meta_fields and 'created' not in meta_fields:
            meta_data[key]['created'] = meta_data[key]['create']
            value.pop('create', None)
        elif 'create' not in meta_fields and 'created' not in meta_fields:
            meta_data[key]['create'] = time_now

        if 'views' not in meta_fields:
            meta_data[key]['views'] = 1
        if 'modified' not in meta_fields:
            meta_data[key]['modified'] = time_now

        # Removing outdated data
        if 'timestamp' in meta_fields:
            value.pop('timestamp', None)
        if 'updated' in meta_fields:
            value.pop('updated', None)

    save_meta(meta_data)
    print('All meta data has been migrated.')

