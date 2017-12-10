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
        meta_data[key]['create'] = time_now
        meta_data[key]['modified'] = time_now
        meta_data[key]['views'] = 1

        # Removing outdated data
        if 'updated' in value.keys():
            value.pop('updated', None)

    save_date(meta_data)
    print('All meta data has been migrated.')


