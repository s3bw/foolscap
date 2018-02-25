from mock import call
from mock import patch

from foolscap import note_content


def test_update_notes():
    pass


def test_save_note():
    pass


def test_export_note():
    pass


def test_view_note():
    pass


def test_delete_note():
    with patch('foolscap.note_content.note_exists') as exists,\
         patch('foolscap.note_content.os'),\
         patch('foolscap.note_content.unique_text', side_effect='note_test'),\
         patch('foolscap.note_content.remove_component') as mock_remove:
        exists.return_value = True
        note_content.delete_note('test_note')
        exists.assert_called_once_with('test_note')
        mock_remove.assert_called_once_with('test_note')


def test_edit_note():
    pass


def test_new_note():
    pass


def test_note_exist_called():
    with patch('foolscap.note_content.note_exists') as exists:
        exists.return_value = False
        note_content.edit_note('test_note')
        exists.assert_called_once_with('test_note')

    with patch('foolscap.note_content.note_exists') as exists:
        exists.return_value = False
        note_content.view_note('test_note')
        exists.assert_called_once_with('test_note')

    with patch('foolscap.note_content.note_exists') as exists:
        exists.return_value = False
        note_content.export_note('test_note')
        exists.assert_called_once_with('test_note')

    with patch('foolscap.note_content.note_exists') as exists,\
         patch('builtins.input') as input_string:
        input_string.return_value = 'second_note'
        # First one has to set as True as it is called sequentially
        exists.side_effect = [True, False]
        expected_calls = [call('second_note'),
                          call('test_note')]

        note_content.move_lines('test_note')
        exists.assert_has_calls(expected_calls)
    
