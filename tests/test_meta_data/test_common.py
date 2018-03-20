import pkg_resources

import pytest
from mock import Mock
from mock import patch
from mock import MagicMock
from mock import mock_open
from mock import call

from tests.data.mock_meta_data import MOCK_COMPONENT

import foolscap.meta_data.common as common
from foolscap.handle_note_io import load_text


def test_upgrade_components():
    with patch('foolscap.meta_data.common.migrate_meta') as mock_migrate:
        common.upgrade_components()

    mock_migrate.assert_called_once()


def test_tag_exists_true():
    with patch('foolscap.meta_data.common.load_tags') as mock_load:
        mock_load.return_value = {'note', 'note_2'}
        result = common.tag_exists('note')

    assert result == True


def test_tag_exists_false():
    with patch('foolscap.meta_data.common.load_tags') as mock_load,\
         patch('foolscap.meta_data.common.fuzzy_guess') as mock_fuzz:
        mock_tags = {'notes', 'note_2'}
        mock_load.return_value = mock_tags
        result = common.tag_exists('note')

    mock_fuzz.assert_called_once_with('note', mock_tags)


def test_note_exists_true():
    with patch('foolscap.meta_data.common.load_meta') as mock_load:
        mock_load.return_value = {'note': 1, 'note_2': 2}
        result = common.note_exists('note')

    assert result == True


def test_note_exists_false():
    mock_meta_data = {'notes': 1, 'note_2': 2}
    with patch('foolscap.meta_data.common.load_meta') as mock_load,\
         patch('foolscap.meta_data.common.fuzzy_guess') as mock_fuzz:
        mock_load.return_value = mock_meta_data
        result = common.note_exists('note')

    mock_fuzz.assert_called_once_with('note', mock_meta_data.keys())


def test_remove_component():
    mock_data = {'note': 1, 'note_2': 2}
    with patch('foolscap.meta_data.common.load_meta') as mock_load,\
         patch('foolscap.meta_data.common.save_meta') as mock_save:
        mock_load.return_value = mock_data
        common.remove_component('note')

    expected = {'note_2': 2}
    mock_save.assert_called_once_with(expected)
    assert mock_data == expected


def test_add_component():
    mock_data = {'note': 1, 'note_2': 2}
    with patch('foolscap.meta_data.common.load_meta') as mock_load,\
         patch('foolscap.meta_data.common.save_meta') as mock_save:
        mock_load.return_value = mock_data

        component = {'new_note': 3}
        common.add_component(component)

    expected = {'note': 1, 'note_2': 2, 'new_note': 3}
    mock_save.assert_called_once_with(expected)
    assert mock_data == expected


@pytest.mark.parametrize("old_name, new_name, expected",
    [('notes', 'notes', 'notes'),       # no change
     ('notes', 'rename', 'rename'),     # rename, with no conflict
     ('notes', 'note_2', 'note_2_0')])  # rename, with conflict
def test_avoid_conflict(old_name, new_name, expected):
    mock_meta_data = {'notes': 1, 'note_2': 2}
    with patch('foolscap.meta_data.common.unique_text') as mock_unique:
        mock_unique.return_value = new_name + '_0'
        result = common.avoid_conflict(old_name, new_name, mock_meta_data)
    assert result == expected


@pytest.mark.parametrize("old_name, edited_name",
    [('notes', 'notes'),
     ('notes', 'new_name')])
def test_update_note_hooks(old_name, edited_name):
    mock_meta_data = {'notes': 1, 'note_2': 2}
    with patch('foolscap.meta_data.common.load_text'),\
         patch('foolscap.meta_data.common.get_title'),\
         patch('foolscap.meta_data.common.replace_text'),\
         patch('foolscap.meta_data.common.restrict_title') as mck_restrict,\
         patch('foolscap.meta_data.common.get_contents') as mck_content:
        mck_restrict.return_value = edited_name
        mck_content.return_value = ['mock content']
        result = common.update_note_hooks(old_name, mock_meta_data)

    assert result == (edited_name, 'mock content')
    assert mock_meta_data == {edited_name: 1, 'note_2': 2}


def test_update_component():
    component = MOCK_COMPONENT(2, 'no_change').copy()
    with patch('foolscap.meta_data.common.load_meta') as mock_data,\
         patch('foolscap.meta_data.common.update_note_hooks') as mock_hook,\
         patch('foolscap.meta_data.common.note_description') as mock_desc,\
         patch('foolscap.meta_data.common.note_tags') as mock_tags,\
         patch('foolscap.meta_data.common.datetime') as time,\
         patch('foolscap.meta_data.common.save_meta'):
        mock_data.return_value = component
        mock_hook.return_value = ('note', ['note content'])
        mock_desc.return_value = 'This is a fake note'
        mock_tags.return_value = ['fake_tag']
        time.now.return_value = 'new_datetime'

        # These are different from fake component as not has been changed.
        expected = MOCK_COMPONENT(3, 'new_datetime').copy()
        common.update_component('note')
        assert component == expected


def test_new_component():
    mock_note = [
        '',
        '# note',
        '====================',
        ':This is a fake note',
        '',
        'Some content.',
        '',
        '{fake_tag}',
        '====================',
    ]
    with patch('foolscap.meta_data.common.save_text') as mock_save_text,\
         patch('foolscap.meta_data.common.unique_text') as mock_unique_heading,\
         patch('foolscap.meta_data.common.add_component') as mock_add,\
         patch('foolscap.meta_data.common.datetime') as fake_time:
        fake_time.now.return_value = 'created_date'
        mock_unique_heading.return_value = 'note'

        common.new_component(mock_note)
        expected_component = MOCK_COMPONENT(1, 'created_date').copy()

    mock_add.assert_called_once_with(expected_component)
    mock_save_text.assert_called_once()


def test_multiple_new_components():
    mock_note = [
        '',
        '# note',
        '====================',
        ':This is a fake note',
        '',
        'Some content.',
        '',
        '{fake_tag}',
        '====================',
        '',
        '# note_2',
        '====================',
        ':This is a fake note',
        '',
        'Some content.',
        '',
        '{fake_tag}',
        '====================',
    ]
    with patch('foolscap.meta_data.common.save_text') as mock_save_text,\
         patch('foolscap.meta_data.common.unique_text') as mock_unique_heading,\
         patch('foolscap.meta_data.common.add_component') as mock_add,\
         patch('foolscap.meta_data.common.datetime') as fake_time:
        fake_time.now.return_value = 'created_date'
        mock_unique_heading.side_effect = ['note', 'note_2']

        common.new_component(mock_note)

    first_component = MOCK_COMPONENT(1, 'created_date').copy()
    second_component = MOCK_COMPONENT(1, 'created_date').copy()
    calls = [call(first_component), call(second_component)]
    mock_add.has_calls(calls)


EXPECTED_NOTE = """
# test_note
====================
:Description of note

Some content.
>Move content.

{test} {unit}
===================="""
def test_remove_moving_lines():
    note = EXPECTED_NOTE.split('\n')
    expected_content = [
        '',
        '# test_note',
        '====================',
        ':Description of note',
        '',
        'Some content.',
        '',
        '{test} {unit}',
        '====================',
    ]
    result = common.remove_moving_lines(note)
    assert result == expected_content


def test_subheading_components():
    test_note = pkg_resources.resource_filename(
        __name__,
        'data/test_note_subheadings.txt'
    )
    expected = {
        'note': {
            'created': 'created_date',
            'views': 1,
            'modified': 'created_date',
            'description': 'This tests subheadings',
            'tags': ['subheadings', 'test'],
            'sub_headings': [
                ('First test:', ':this is the first sub'),
                ('Second test:', ':this is the 2nd sub')],
            'num_sub': 2
        }
    }
    with patch('foolscap.meta_data.common.save_text') as mock_save_text,\
         patch('foolscap.meta_data.common.unique_text') as mock_unique_heading,\
         patch('foolscap.meta_data.common.add_component') as mock_add,\
         patch('foolscap.meta_data.common.datetime') as fake_time:
        mock_note = load_text(test_note, new_note=True)

        fake_time.now.return_value = 'created_date'
        mock_unique_heading.return_value = 'note'

        common.new_component(mock_note)

    mock_add.assert_called_once_with(expected)
    mock_save_text.assert_called_once()

