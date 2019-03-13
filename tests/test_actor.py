from mock import call
from mock import patch
from mock import MagicMock

import pytest

from fool.console import ConsoleReturn
from foolscap import actor

ACTIONS = actor.FUNCTION_MAP.keys()
TESTED_ACTIONS = []


class MockCtrl:
    def __init__(self, model_type):
        self.model_type = model_type

    def basic_output(self):
        return ConsoleReturn('view', key='note')

    def query_output(self, query):
        return ConsoleReturn('view', key='note')

    def search_output(self, query):
        return ConsoleReturn('view', key='note')


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


@pytest.mark.parametrize(
    "query, expected",
    # Test with Query = 'te'
    [('te', [call('te')])])
def test_search_note(query, expected):
    TESTED_ACTIONS.append('search')
    mock_view = MagicMock()
    mock_ctrl = MagicMock()
    # Have to return view so that we can exit
    mock_ctrl.return_value.\
        search_output.return_value = ConsoleReturn('view', key='mock_note')
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_view}),\
            patch('foolscap.actor.Controller', mock_ctrl):

        # Pass to actor:
        actor.action('search', query)
        assert mock_ctrl.call_args_list == [call('notes')]
        assert mock_ctrl.return_value.search_output.call_args_list == expected


def test_list_note_command_no_tags():
    TESTED_ACTIONS.append('list')
    mock_view = MagicMock()
    mock_ctrl = MagicMock()
    # Have to return view so that we can exit
    mock_ctrl.return_value.\
        basic_output.return_value = ConsoleReturn('view', key='mock_note')
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_view}),\
            patch('foolscap.actor.Controller', mock_ctrl):

        # Pass to actor:
        actor.action('list', None)
        mock_ctrl.return_value.basic_output.assert_called()


def test_list_note_command_returning_func():
    mock_view = MagicMock()
    mock_ctrl = MagicMock()
    # Have to return view so that we can exit
    mock_ctrl.return_value.\
        query_output.return_value = ConsoleReturn('view', key='mock_note')
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_view}),\
            patch('foolscap.actor.Controller', mock_ctrl):

        expected_view = call('mock_note')

        actor.action('list', 'tag')
        # If list function returns a new-action:
        # this case view
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
    with patch.dict('foolscap.actor.FUNCTION_MAP',
                    {'move_lines': mock_action}):
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


def test_change_book():
    """Test that book can change."""
    mock_view = MagicMock()
    mock_ctrl = MagicMock()
    # Have to return view so that we can exit
    mock_ctrl.return_value.basic_output.side_effect = [
        ConsoleReturn('list', value='mock_book', key='note'),
        ConsoleReturn('list', key='note'),
    ]

    mock_functions = {
        'view': mock_view,
        'list': None,
    }
    with patch.dict('foolscap.actor.FUNCTION_MAP', mock_functions),\
            patch('foolscap.actor.Controller', mock_ctrl):

        actor.action('list', None)
        mock_ctrl.has_calls(calls=[call('general'), call('mock_book')])
        mock_ctrl.return_value.basic_output.assert_called()


def test_change_list_type():
    mock_view = MagicMock()
    mock_ctrl = MagicMock()
    # Have to return view so that we can exit
    mock_ctrl.return_value.\
        basic_output.return_value = ConsoleReturn('view', key='note')
    with patch.dict('foolscap.actor.FUNCTION_MAP', {'view': mock_view}),\
            patch('foolscap.actor.Controller', mock_ctrl):

        actor.action('list', None, 'tags')
        mock_ctrl.assert_called_with('tags')
        mock_ctrl.return_value.basic_output.assert_called()
