from mock import call
from mock import patch
from mock import MagicMock

from foolscap import actor


FAKE_META_DATA = 'mock_data'


def test_save_note_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'save': mock_action}):
        # Save expects the following:
        expected = call('mock_note.txt', FAKE_META_DATA)

        # Pass to actor:
        actor.action('save', FAKE_META_DATA, 'mock_note.txt')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_view_note_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_action}):
        # View expects the following:
        expected = call('mock_note', FAKE_META_DATA)

        # Pass to actor:
        actor.action('view', FAKE_META_DATA, 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected 


def test_list_note_command_no_tags():
    mock_action = MagicMock()
    with  patch.dict('foolscap.actor.FUNCTION_MAP', {'list': mock_action}):
        mock_action.return_value = None
        # List with no tags expects:
        # This is tricky, as list calls exit() if it quits in menu object
        # but cause we don't call the menu object, we return None
        # and have to expect the func to be called again...
        expected = [call(None, FAKE_META_DATA), call(FAKE_META_DATA)]

        # Pass to actor:
        actor.action('list', FAKE_META_DATA, None)
        assert mock_action.call_args_list == expected


def test_list_note_command_tags():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'list': mock_action}):
        mock_action.return_value = None
        # List with tags expects:
        # Note: same as last test.
        expected = [
            call('tag', FAKE_META_DATA), 
            call('tag', FAKE_META_DATA)
        ]

        # Pass to actor:
        actor.action('list', FAKE_META_DATA, 'tag')
        assert mock_action.call_args_list == expected


def test_list_note_command_returning_func():
    mock_list = MagicMock()
    mock_view = MagicMock()
    mock_function_map = {
        'list': mock_list,
        'view': mock_view
    }
    with patch.dict('foolscap.actor.FUNCTION_MAP', mock_function_map):
        # If list function returns a new-action:
        mock_list.return_value = ('view', 'mock_note')

        expected_list = call('tag', FAKE_META_DATA)
        expected_view = call('mock_note', FAKE_META_DATA)

        actor.action('list', FAKE_META_DATA, 'tag')
        assert mock_list.call_args == expected_list
        assert mock_view.call_args == expected_view
        mock_view.assert_called_once()


def test_edit_note_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'edit': mock_action}):
        # Edit expects the following:
        expected = call('mock_note', FAKE_META_DATA)

        # Pass edit to actor.
        actor.action('edit', FAKE_META_DATA, 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_delete_note_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'delete': mock_action}):
        # Delete expects:
        expected = call('mock_note', FAKE_META_DATA)
         
        actor.action('delete', FAKE_META_DATA, 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_new_note_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'new': mock_action}):
        # New expects:
        expected = call(FAKE_META_DATA)
         
        actor.action('new', FAKE_META_DATA, None)
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_move_lines_command():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'move_lines': mock_action}):
        # Move Lines expects:
        expected = call('mock_note', FAKE_META_DATA)
         
        actor.action('move_lines', FAKE_META_DATA, 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected

def test_pass_none_existing_action():
    # Handled in CLI argparse
    pass
