from mock import call
from mock import patch
from mock import MagicMock

from foolscap.cli import main


# foolscap.cli.note_data
FAKE_DATA = 'mock_data'


def make_test_args(tup):
    sample_args = ['foolscap/cli.py']
    sample_args.extend(tup)
    return sample_args


def test_save_note_command():
    test_args = make_test_args(['save', 'mock_note.txt'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'save': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        expected = call('mock_note.txt', FAKE_DATA)
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == expected


def test_save_note_fail_command():
    test_args = make_test_args(['save'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'save': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        expected = call('mock_note.txt', FAKE_DATA)
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args != expected


def test_view_note_command():
    test_args = make_test_args(['view', 'mock_note'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'view': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == (('mock_note', FAKE_DATA),)


def test_list_note_command_no_tags():
    test_args = make_test_args(['list'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'list': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == ((None, FAKE_DATA),)


def test_list_note_command_tags():
    test_args = make_test_args(['list', 'code'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'list': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == (('code', FAKE_DATA),)


def test_edit_note_command():
    test_args = make_test_args(['edit', 'mock_note'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'edit': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == (('mock_note', FAKE_DATA),)


def test_delete_note_command():
    test_args = make_test_args(['delete', 'mock_note'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'delete': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == (('mock_note', FAKE_DATA),)


def test_new_note_command():
    test_args = make_test_args(['new'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'new': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        print(mock_action.call_args)
        assert mock_action.call_args == call(FAKE_DATA)


def test_move_lines_command():
    test_args = make_test_args(['move_lines', 'mock_note'])
    mock_action = MagicMock()
    with patch('sys.argv', test_args),\
         patch.dict('foolscap.cli.FUNCTION_MAP', {'move_lines': mock_action}),\
         patch('foolscap.cli.load_data', side_effect=[FAKE_DATA]):
        main()
        mock_action.assert_called_once()
        assert mock_action.call_args == (('mock_note', FAKE_DATA),)
