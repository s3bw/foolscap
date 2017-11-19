import pkg_resources
from mock import patch, Mock

import foolscap.parse_text as parse_text


TEST_NOTE = pkg_resources.resource_filename(
    __name__,
    'data/test_note.txt'
)

EXPECTED_NOTE = """
# note_is_test
====================
:Description of note

Some content.
>Move content.

{test} {unit}
====================

"""


# I should do multiple notes with different results,
# No lines to move, lines to move.
# What happens with no title?
# also "section" needs to be renamed to "title"
#   \-> Section renamed to description and make a parsing of sub_headings.


def test_load_text():
    note = parse_text.load_text(TEST_NOTE)

    assert note == EXPECTED_NOTE.split('\n')
    assert len(note) == 12


# def test_edit_text():
  #   note = parse_text.edit_text(TEST_NOTE)
  #   assert note == EXPECTED_NOTE.split('\n')
  #   assert len(note) == 12


def test_unique_heading():
    with patch('foolscap.parse_text.os.listdir') as mock_saved:
        mock_saved.return_value = ['test_note.txt', 'mock_note.txt']
        # return note name if it's not in list:
        assert parse_text.unique_heading('not_here') == 'not_here'
        # append _0 if in list:
        assert parse_text.unique_heading('test_note') == 'test_note_0'
        # do not return the same thing if in list:
        assert parse_text.unique_heading('mock_note') != 'mock_note'


# def test_save_text():
#   This needs to check it returns heading.
#   


def test_get_titles():
    note = EXPECTED_NOTE.split('\n')

    section = parse_text.get_title(note)
    assert section == ['note_is_test']
    assert len(section) == 1


def test_get_moving_lines():
    note = EXPECTED_NOTE.split('\n')

    moving_lines = parse_text.get_moving_lines(note)
    assert moving_lines == ['>Move content.']


def test_remove_moving_lines():
    note = EXPECTED_NOTE.split('\n')
    expected_content = [
        '',
        '# note_is_test',
        '====================', 
        ':Description of note', 
        '', 
        'Some content.', 
        '', 
        '{test} {unit}', 
        '====================',
        '',
        ''
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


def test_note_component():
    with patch('foolscap.parse_text.save_text') as mock_save_text,\
    patch('foolscap.parse_text.unique_heading') as mock_unique_heading:
        mock_unique_heading.return_value = 'note_is_test'
        note = EXPECTED_NOTE.split('\n')
        component = parse_text.note_component(note)
        expected_component = {
            'note_is_test': {
                'timestamp': 'now',
                'description': 'Description of note',
                'tags': ['test', 'unit'],
            }
        }
        assert component == expected_component
        mock_save_text.assert_called_once()


SHIFT_FROM_NOTE = """
# remove_lines
====================
:Description of note

Some content.
>Move content.

{test} {unit}
====================
"""

SHIFT_TO_NOTE = """
# get_lines
====================
:Description of note

Some content.

{test} {unit}
====================
"""

fake_responses = [Mock(), Mock()]
fake_responses[0].return_value = SHIFT_FROM_NOTE.split('\n')
fake_responses[1].return_value = SHIFT_TO_NOTE.split('\n')

fake_responses = SHIFT_FROM_NOTE.split('\n')# , SHIFT_TO_NOTE.split('\n')]

def test_shift_lines():
    with patch('foolscap.parse_text.load_text') as mock_load_text,\
    patch('foolscap.parse_text.save_text'),\
    patch('foolscap.parse_text.os.remove'): #,\
        mock_load_text.side_effect = (SHIFT_FROM_NOTE.split('\n'), SHIFT_TO_NOTE.split('\n'))
        print(parse_text.shift_lines('fake_it', 'make_it'))
        
        

        # mock_load_text.return_value = SHIFT_FROM_NOTE.split('\n')

    # Setup:
        # Two temp notes, with content
        # Assert that the notes end up as expected.
        # In the integration test - test that error is raised for typos!

    # note = EXPECTED_NOTE.split('\n')


# def test_update_component():

