import os

import pkg_resources
import pytest
from mock import Mock
from mock import patch
from mock import MagicMock
from mock import mock_open

import foolscap.parse_text as parse_text
from foolscap.file_paths import NOTE_FOLDERS


TITLE_LEN = parse_text.MAX_TITLE_LEN


TEST_NOTE = pkg_resources.resource_filename(
    __name__,
    'data/test_note.txt'
)

EXPECTED_NOTE = """
# test_note
====================
:Description of note

Some content.
>Move content.

{test} {unit}
===================="""

TEST_NOTE_TEMPLATE = """\
# title
==========
: description
Make sure you change the title!


{tag}
=========="""


# I should do multiple notes with different results,
# No lines to move, lines to move.
# What happens with no title?
# also "section" needs to be renamed to "title"
#   \-> Section renamed to description and make a parsing of sub_headings.


def test_load_text():
    note = parse_text.load_text(TEST_NOTE)

    assert note == EXPECTED_NOTE.split('\n')
    assert len(note) == 10


def test_edit_temp_text():
    temp_note = parse_text.NEW_NOTE_TEMPLATE
    with patch('foolscap.parse_text.NamedTemporaryFile', mock_open(read_data=temp_note)),\
         patch('foolscap.parse_text.edit_in_vim'),\
         patch('builtins.open', mock_open()) as mock_file:
        note = parse_text.edit_text()
        assert note == TEST_NOTE_TEMPLATE.split('\n')
        assert not mock_file.called


def test_edit_text():
    with patch('foolscap.parse_text.NamedTemporaryFile'),\
         patch('foolscap.parse_text.edit_in_vim'),\
         patch('builtins.open', mock_open()) as mock_file:
        note = parse_text.edit_text('test_note.txt')
        assert note == None
        mock_file.assert_called_with('test_note.txt', 'r')


def test_unique_heading():
    with patch('foolscap.parse_text.os.listdir') as mock_saved:
        mock_saved.return_value = ['test_note.txt', 'mock_note.txt']
        # return note name if it's not in list:
        assert parse_text.unique_heading('not_here') == 'not_here'
        # append _0 if in list:
        assert parse_text.unique_heading('test_note') == 'test_note_0'
        # do not return the same thing if in list:
        assert parse_text.unique_heading('mock_note') != 'mock_note'


def test_save_text():
    with patch('builtins.open', mock_open()) as mock_file:
        note_title = 'test_title'
        expected = NOTE_FOLDERS['GET_NOTE'].format(note_name=note_title)

        parse_text.save_text(note_title, ['Note', 'content.'])
        mock_file.assert_called_with(expected, 'w')


def test_replace_spaces():
    result = parse_text.replace_spaces('note title')
    assert result == 'note_title'


def test_max_title_len():
    test_title = 'note_title_which_is_a_little_too_long'
    result = parse_text.max_title_len(test_title)
    assert result == test_title[:TITLE_LEN]


def test_restict_title():
    result = parse_text.restrict_title('note title')
    assert result == 'note_title'


def test_get_titles():
    note = EXPECTED_NOTE.split('\n')

    section = parse_text.get_title(note)
    assert section == ['test_note']
    assert len(section) == 1


def test_get_moving_lines():
    note = EXPECTED_NOTE.split('\n')

    moving_lines = parse_text.get_moving_lines(note)
    assert moving_lines == ['>Move content.']


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
    result = parse_text.remove_moving_lines(note)
    assert result == expected_content


def test_pairwise():
    input_arg = [1, 2, 3, 4]
    result = list(parse_text.pairwise(input_arg))
  
    assert result == [(1, 2), (3, 4)]


def test_note_description():
    fake_content = ['', ':Description of note', '']
    description = parse_text.note_description(fake_content)
    assert description == 'Description of note'

    fake_content = ['', ':    My awesome note', '']
    result = parse_text.note_description(fake_content)
    assert result == 'My awesome note'


def test_note_tags():
    note = EXPECTED_NOTE.split('\n')
    content = parse_text.get_contents(note)[0]
    tags = parse_text.note_tags(content)
    expected_tags = ['test', 'unit']
    assert tags == expected_tags


def test_get_contents():
    note = EXPECTED_NOTE.split('\n')
    content = parse_text.get_contents(note)
    expected_content = [[
        '====================', 
        ':Description of note', 
        '', 
        'Some content.', 
        '>Move content.', 
        '', 
        '{test} {unit}', 
        '===================='
    ]]
    assert content == expected_content


@pytest.mark.parametrize("mock_content,expected",
    [([ '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],[2]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],[2,5]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        'testing subtitles',
        '',
        '===================='],[])])
def test_index_sub_headings(mock_content, expected):
    result = parse_text.index_sub_headings(mock_content)
    assert result == expected

@pytest.mark.parametrize("mock_content,expected",
    [([ '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],
        [('Sub Title:', ':testing subtitles')]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],
        [('Sub Title:', ':testing subtitles'),
         ('Sub Title:', ':testing subtitles')]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        'testing subtitles',
        '',
        '===================='],
        [])])
def test_parse_sub_headings(mock_content, expected):
    result = parse_text.parse_sub_headings(mock_content)
    assert result == expected


def test_note_component():
    with patch('foolscap.parse_text.save_text') as mock_save_text,\
    patch('foolscap.parse_text.unique_heading') as mock_unique_heading,\
    patch('foolscap.parse_text.datetime') as fake_time:
        fake_time.now.return_value = 'now'
        mock_unique_heading.return_value = 'note_is_test'

        note = EXPECTED_NOTE.split('\n')
        component = parse_text.note_component(note)
        # Decompose and parametize with notes of different entries (sub-titles tags descriptions)
        expected_component = {
            'note_is_test': {
                'description': 'Description of note',
                'tags': ['test', 'unit'],
                'created': 'now',
                'modified': 'now',
                'views': 1
            }
        }
        assert component == expected_component
        mock_save_text.assert_called_once()



# def test_shift_lines():


FAKE_COMPONENT = {
    'test_note': {
        'description': 'description',
        'tags': ['tag', 'unit'],
        'created': 'datetime',
        'modified': 'datetime',
        'views': 2,
    }
}
# This needs to be decomposed and thoroughly tested.
def test_update_component():
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    NOTE_STORAGE = os.path.join('data', '{note_name}.txt')
    NOTES = os.path.join(SCRIPT_DIR, NOTE_STORAGE)
    new_value = {'GET_NOTE': NOTES}
    with patch.dict('foolscap.parse_text.NOTE_FOLDERS', new_value),\
         patch('foolscap.parse_text.datetime') as time:
        time.now.return_value = 'new_datetime'
        component = FAKE_COMPONENT.copy()
        # These are different from fake component as not has been changed.
        expected = {
            'test_note': {
                'description': 'Description of note',
                'tags': ['test', 'unit'],
                'created': 'datetime',
                'modified': 'new_datetime',
                'views': 3,
            }
        }
        result = parse_text.update_component('test_note', component)
        print(result)
        print(expected)
        assert result == expected

