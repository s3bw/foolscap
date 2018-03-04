import pytest
from mock import call
from mock import patch
from mock import Mock
from mock import MagicMock

from foolscap.display.console import display_list
from foolscap.display.console import setup_folio
from foolscap.display.console import FolioConsole


FAKE_ITEMS = [
    {'title': "test_title", 'description': "test description"},
    {'title': "another_title", 'description': "another description"},
]


def test_display_list():
    with patch('foolscap.display.console.setup_folio', 'func()'),\
         patch('foolscap.display.console.curses') as mock_curses:
        result = display_list('fake_data')
        mock_curses.wrapper.assert_called_with('func()', 'fake_data')


def test_setup_folio():
    mock_screen = MagicMock()
    fake_data = FAKE_ITEMS
    with patch('foolscap.display.console.FolioConsole') as mock_folio,\
         patch('foolscap.display.console.curses') as mock_curses:
        calls = [call(mock_screen, FAKE_ITEMS),
                 call().__enter__(),
                 call().__enter__().show(),
                 call().__exit__(None, None, None)]

        result = setup_folio(mock_screen, fake_data)
        mock_curses.curs_set.assert_called_with(0)
        assert mock_folio.mock_calls == calls


def test_FolioConsole_contextmanager():
    two_calls = [call(), call()]
    mock_screen = MagicMock()
    mock_screen.subwin(0,0).getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel') as mock_panel,\
         patch('foolscap.display.console.curses') as mock_curses:
        with FolioConsole(mock_screen, FAKE_ITEMS) as folio_console:
            mock_screen.subwin().keypad.assert_called_once() 
            mock_screen.subwin().clear.assert_called_once() 

            mock_panel.update_panels.assert_called_once() 
            mock_panel.new_panel().hide.assert_called_once() 
            mock_panel.new_panel().top.assert_called_once() 
            mock_panel.new_panel().show.assert_called_once() 
        
        assert mock_screen.subwin().clear.mock_calls == two_calls
        assert mock_panel.new_panel().hide.mock_calls == two_calls
        assert mock_panel.update_panels.mock_calls == two_calls
        mock_curses.doupdate.assert_called_once()



@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayContents')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_init(mock_keys, mock_display, mock_titlebar,
                           mock_statusbar, mock_helpbar, mock_frame):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel') as mock_panel,\
         patch('foolscap.display.console.curses') as mock_curses:
        mocked_render_objects = [
            mock_frame(),
            mock_statusbar(),
            mock_titlebar(),
            mock_helpbar(),
            mock_display(),
        ]

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        assert hasattr(test_console, 'render_objects')
        assert hasattr(test_console, 'items')
        assert hasattr(test_console, 'screen')
        assert hasattr(test_console, 'panel')
        assert hasattr(test_console, 'count_notes')

        assert hasattr(test_console, 'list_content')
        assert hasattr(test_console, 'key_listener')

        assert test_console.items == FAKE_ITEMS
        assert test_console.count_notes == 2
        assert test_console.render_objects == mocked_render_objects
        assert len(test_console.render_objects) == 5
        assert test_console.key_listener == mock_keys()

        mock_frame.assert_called_with(mock_screen.subwin())
        mock_statusbar.assert_called_with(mock_screen.subwin(), 2)
        mock_titlebar.assert_called_with(mock_screen.subwin())
        mock_helpbar.assert_called_with(mock_screen.subwin())
        mock_display.assert_called_with(mock_screen.subwin(), FAKE_ITEMS)


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayContents')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_render(mock_listener, mock_display, mock_titlebar,
                           mock_statusbar, mock_helpbar, mock_frame):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel') as mock_panel,\
         patch('foolscap.display.console.curses') as mock_curses:
        mocked_render_objects = [
            mock_frame(),
            mock_statusbar(),
            mock_titlebar(),
            mock_helpbar(),
            mock_display(),
        ]

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        test_console.render_all()
        mock_screen.subwin().clear.assert_called_once()
        for mock_obj in mocked_render_objects:
            mock_obj.update.assert_called_once()
            mock_obj.draw.assert_called_once()


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayContents')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_show(mock_listener, mock_display, mock_titlebar,
                           mock_statusbar, mock_helpbar, mock_frame):
    mock_screen = MagicMock()
    with patch('foolscap.display.console.panel') as mock_panel,\
         patch('foolscap.display.console.curses') as mock_curses:
        mocked_render_objects = [
            mock_frame(),
            mock_statusbar(),
            mock_titlebar(),
            mock_helpbar(),
            mock_display(),
        ]
        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        with patch.object(test_console, 'key_listener') as mocked_listener:
            mock_position = (0, 1)
            mocked_listener.get_position.return_value = mock_position
            mocked_listener.get_action.return_value = ('action', 1, None)

            result = test_console.show()
            mock_display().update_pointers.assert_called_with(mock_position[0], mock_position[1])

