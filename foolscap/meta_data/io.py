import os
import pickle
from datetime import datetime

from foolscap.file_paths import NOTE_DATA
from foolscap.file_paths import BACKUP_DATA
from foolscap.file_paths import TAG_DATA


TAG_HISTORY = 50
RECORD_DELETION = "{{{tag}}} -remove-from- {note} {date}"
RECORD_ADDITION = "{{{tag}}} +added+to+ {note} {date}"


def record_tags(note, deleted, added):
    if not os.path.isfile(TAG_DATA):
        open(TAG_DATA, 'a').close()

    now = datetime.now().strftime("%Y-%m-%d")

    changes = len(deleted | added)
    history_len = sum(1 for line in open(TAG_DATA))
    remove_lines = 0
    if history_len + changes > TAG_HISTORY:
        remove_lines = history_len + changes - TAG_HISTORY

    deletions = [
        RECORD_DELETION.format(tag=delete, note=note, date=now)
        for delete in deleted
    ]
    additions = [
        RECORD_ADDITION.format(tag=add, note=note, date=now)
        for add in added
    ]
    with open(TAG_DATA, 'r') as _file_in:
        data = _file_in.read().splitlines()
    data += deletions + additions
    with open(TAG_DATA, 'w') as _file_out:
        _file_out.write('\n'.join(data[remove_lines:]))


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

    # I need to handle this error better
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
            meta_data[key]['created'] = time_now

        if 'views' not in meta_fields:
            meta_data[key]['views'] = 1
        if 'modified' not in meta_fields:
            meta_data[key]['modified'] = time_now
        if 'book' not in meta_fields:
            meta_data[key]['book'] = 'general'

        # Removing outdated data
        if 'timestamp' in meta_fields:
            value.pop('timestamp', None)
        if 'updated' in meta_fields:
            value.pop('updated', None)

        if 'sub_headings' in meta_fields:
            # Sub heading indexes given a dummy value on migration.
            sh = meta_data[key]['sub_headings']
            meta_data[key]['sub_headings'] = [(n[0], n[1], 1, 1) for n in sh]
            meta_data[key]['num_sub'] = len(
                meta_data[key]['sub_headings']
            )

    save_meta(meta_data)
    print('All meta data has been migrated.')

