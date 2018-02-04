import pkg_resources

from mock import patch
from mock import mock_open

import foolscap.handle_note_io as handle_note_io


TEST_NOTE = pkg_resources.resource_filename(
    __name__,
    'data/{note_name}.txt'
)


def test_load_text():
    """ Title upper case to check for convert to lower
    in other tests.
    """
    test_folder = {'GET_NOTE': TEST_NOTE}
    with patch.dict('foolscap.handle_note_io.NOTE_FOLDERS', test_folder):
        note = handle_note_io.load_text('test_note')
        expected_note = [
            '',
            '# TEST_NOTE',
            '====================',
            ':Description of note',
            '',
            'Some content.',
            '>Move content.',
            '',
            '{test} {unit}',
            '====================',
            '',
        ]
        assert note == expected_note
        assert len(note) == 11


def test_save_text():
    test_folder = {'GET_NOTE': TEST_NOTE}
    with patch.dict('foolscap.handle_note_io.NOTE_FOLDERS', test_folder),\
         patch('builtins.open', mock_open()) as mock_file:
        note_title = 'test_title'
        expected = TEST_NOTE.format(note_name=note_title)
        handle_note_io.save_text(note_title, ['Note', 'content.'])
        mock_file.assert_called_with(expected, 'w')


def test_unique_heading():
    with patch('foolscap.handle_note_io.os.listdir') as mock_saved,\
         patch('foolscap.handle_note_io.NOTE_FOLDERS'): 
        mock_saved.return_value = ['test_note.txt', 'mock_note.txt']
        # return note name if it's not in list:
        assert handle_note_io.unique_text('not_here') == 'not_here'
        # append _0 if in list:
        assert handle_note_io.unique_text('test_note') == 'test_note_0'
        # do not return the same thing if in list:
        assert handle_note_io.unique_text('mock_note') != 'mock_note'


def test_edit_text():
    with patch('foolscap.handle_note_io.NamedTemporaryFile'),\
         patch('foolscap.handle_note_io.edit_in_vim'),\
         patch('builtins.open', mock_open()) as mock_file:
        note = handle_note_io.edit_text('test_note.txt')
        assert note == None
        mock_file.assert_called_with('test_note.txt', 'r')


TEST_NOTE_TEMPLATE = """\
# title
==========
: description
Make sure you change the title!


{tag}
=========="""
def test_edit_temp_text():
    temp_note = handle_note_io.NEW_NOTE_TEMPLATE
    with patch('foolscap.handle_note_io.NamedTemporaryFile', mock_open(read_data=temp_note)),\
         patch('foolscap.handle_note_io.edit_in_vim'),\
         patch('builtins.open', mock_open()) as mock_file:
        note = handle_note_io.edit_text()
        assert note == TEST_NOTE_TEMPLATE.split('\n')
        assert not mock_file.called

