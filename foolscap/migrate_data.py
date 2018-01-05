from datetime import datetime

from meta_data import save_data


def update_version(meta_data):
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

    # Backup data before migrating
    save_data(meta_data, backup=True)
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

    save_data(meta_data)
    print('All meta data has been migrated.')

