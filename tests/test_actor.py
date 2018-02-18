from mock import call
from mock import patch
from mock import MagicMock

from foolscap import actor


ACTIONS = actor.FUNCTION_MAP.keys()
TESTED_ACTIONS = []


def test_save_note_command():
    TESTED_ACTIONS.append('save')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'save': mock_action}):
        # Save expects the following:
        expected = call('mock_note.txt')

        # Pass to actor:
        actor.action('save', 'mock_note.txt')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_view_note_command():
    TESTED_ACTIONS.append('view')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_action}):
        # View expects the following:
        expected = call('mock_note')

        # Pass to actor:
        actor.action('view', 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_export_note_command():
    TESTED_ACTIONS.append('export')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'export': mock_action}):
        # export expects the following:
        expected = call('mock_note')

        # Pass to actor:
        actor.action('export', 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_list_note_command_no_tags():
    TESTED_ACTIONS.append('list')
    mock_action = MagicMock()
    with  patch.dict('foolscap.actor.FUNCTION_MAP', {'list': mock_action}):
        mock_action.return_value = None
        # List with no tags expects:
        # This is tricky, as list calls exit() if it quits in menu object
        # but cause we don't call the menu object, we return None
        # and have to expect the func to be called again...
        expected = [call(None, 'normal'), call()]

        # Pass to actor:
        actor.action('list', None)
        assert mock_action.call_args_list == expected


def test_list_note_command_tags():
    TESTED_ACTIONS.append('list')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'list': mock_action}):
        mock_action.return_value = None
        # List with tags expects:
        # Note: same as last test.
        expected = [
            call('tag', 'normal'),
            call('tag')
        ]

        # Pass to actor:
        actor.action('list', 'tag')
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

        expected_list = call('tag', 'normal')
        expected_view = call('mock_note')

        actor.action('list', 'tag')
        assert mock_list.call_args == expected_list
        assert mock_view.call_args == expected_view
        mock_view.assert_called_once()


def test_edit_note_command():
    TESTED_ACTIONS.append('edit')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'edit': mock_action}):
        # Edit expects the following:
        expected = call('mock_note')

        # Pass edit to actor.
        actor.action('edit', 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_delete_note_command():
    TESTED_ACTIONS.append('delete')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'delete': mock_action}):
        # Delete expects:
        expected = call('mock_note')

        actor.action('delete', 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_new_note_command():
    TESTED_ACTIONS.append('new')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'new': mock_action}):
        # New expects:
        expected = call()

        actor.action('new', None)
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_move_lines_command():
    TESTED_ACTIONS.append('move_lines')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'move_lines': mock_action}):
        # Move Lines expects:
        expected = call('mock_note')

        actor.action('move_lines', 'mock_note')
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_migrate_command():
    TESTED_ACTIONS.append('migrate')
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'migrate': mock_action}):
        expected = call()
        actor.action('migrate', None)
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_all_actions():
    assert set(ACTIONS) == set(TESTED_ACTIONS)


def test_change_list_type():
    mock_action = MagicMock()
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'list': mock_action}):
        mock_action.return_value = None
        expected = [
            call(None, 'tags'),
            call()
        ]
        actor.action('list', None, 'tags')
        assert mock_action.call_args_list == expected
