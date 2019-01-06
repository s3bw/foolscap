from mock import call
from mock import patch
from mock import MagicMock

from foolscap.display.console import display_list
from foolscap.display.console import setup_folio
from foolscap.display.console import FolioConsole

mock_model = MagicMock()
FAKE_ITEMS = {
    'titles': ["test_title", "another_title"],
    'model': mock_model,
    'books': ['general', 'work'],
    'tab_title': 'general',
}


def test_display_list():
    with patch('foolscap.display.console.setup_folio', 'func()'),\
            patch('foolscap.display.console.curses') as mock_curses:
        display_list('fake_data')
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

        setup_folio(mock_screen, fake_data)
        mock_curses.curs_set.assert_called_with(0)
        assert mock_folio.mock_calls == calls


def test_FolioConsole_contextmanager():
    two_calls = [call(), call()]
    mock_screen = MagicMock()
    mock_screen.subwin(0, 0).getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel') as mock_panel,\
            patch('foolscap.display.console.curses') as mock_curses:
        with FolioConsole(mock_screen, FAKE_ITEMS):
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
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_init(mock_keys, mock_tab, mock_display_menu,
                           mock_titlebar, mock_statusbar, mock_helpbar,
                           mock_frame):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):
        mocked_render_objects = [
            mock_frame(),
            mock_statusbar(),
            mock_titlebar(),
            mock_helpbar(),
            mock_tab(),
            mock_display_menu(),
        ]

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        assert hasattr(test_console, 'render_objects')
        assert hasattr(test_console, 'items')
        assert hasattr(test_console, 'screen')
        assert hasattr(test_console, 'panel')

        assert hasattr(test_console, 'help_bar')
        assert hasattr(test_console, 'menu')
        assert hasattr(test_console, 'key_listener')

        assert test_console.items == FAKE_ITEMS['titles']
        assert test_console.render_objects == mocked_render_objects
        assert len(test_console.render_objects) == 6
        assert test_console.key_listener == mock_keys()

        mock_frame.assert_called_with(mock_screen.subwin())
        mock_statusbar.assert_called_with(
            mock_screen.subwin(),
            FAKE_ITEMS['titles'], FAKE_ITEMS['model'])
        mock_titlebar.assert_called_with(mock_screen.subwin())
        mock_helpbar.assert_called_with(mock_screen.subwin())
        mock_tab.assert_called_with(
            mock_screen.subwin(), 'general', ['general', 'work'])
        mock_display_menu.assert_called_with(
            mock_screen.subwin(), FAKE_ITEMS['titles'], FAKE_ITEMS['model'])


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_render(mock_listener, mock_tab, mock_display_menu,
                             mock_titlebar, mock_statusbar, mock_helpbar,
                             mock_frame):
    """Test that render objects are updated and drawn."""
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):

        mocked_render_objects = [
            mock_frame(),
            mock_statusbar(),
            mock_titlebar(),
            mock_helpbar(),
            mock_tab(),
            mock_display_menu(),
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
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_show(mock_listener, mock_tab, mock_display_menu,
                           mock_titlebar, mock_statusbar, mock_helpbar,
                           mock_frame):
    mock_screen = MagicMock()
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        with patch.object(test_console, 'key_listener') as mocked_listener:
            mock_position = (0, 1)
            mocked_listener.get_position.return_value = mock_position
            mocked_listener.get_action.return_value = ('action', 1)
            mock_display_menu().select_item.return_value = 'selected_note'

            result = test_console.show()
            mock_display_menu().update_pointers.assert_called_with(
                mock_position[0], mock_position[1])
            assert result == {
                'action': 'action',
                'index': 1,
                'item': 'selected_note'
            }


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_expand_item(mock_listener, mock_tab, mock_display_menu,
                                  mock_titlebar, mock_statusbar, mock_helpbar,
                                  mock_frame):
    mock_screen = MagicMock()
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        with patch.object(test_console, 'key_listener') as mocked_listener:
            mock_position = (0, 1)
            mocked_listener.get_position.return_value = mock_position
            mocked_listener.get_action.side_effect = [
                ('expand', 1), ('action', 1)
            ]
            mock_display_menu().select_item.return_value = 'selected_note'

            test_console.show()
            assert test_console.menu.expand_item.call_args_list == [call(1)]
            test_console.menu.expand_item.assert_called_once()


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_show_help(mock_listener, mock_tab, mock_display_menu,
                                mock_titlebar, mock_statusbar, mock_helpbar,
                                mock_frame):
    mock_screen = MagicMock()
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        with patch.object(test_console, 'key_listener') as mocked_listener:
            mock_position = (0, 1)
            mocked_listener.get_position.return_value = mock_position
            mocked_listener.get_action.side_effect = [
                ('help', 1), ('action', 1)
            ]
            mock_display_menu().select_item.return_value = 'selected_note'

            test_console.show()
            assert test_console.help_bar.next_hint.call_args_list == [call()]
            test_console.help_bar.next_hint.assert_called_once()


@patch('foolscap.display.console.Frame')
@patch('foolscap.display.console.HelpBar')
@patch('foolscap.display.console.StatusBar')
@patch('foolscap.display.console.TitleBar')
@patch('foolscap.display.console.DisplayMenu')
@patch('foolscap.display.console.TabBar')
@patch('foolscap.display.console.KeyListener')
def test_FolioConsole_change_tab(mock_listener, mock_tab, mock_display_menu,
                                 mock_titlebar, mock_statusbar, mock_helpbar,
                                 mock_frame):
    mock_screen = MagicMock()
    with patch('foolscap.display.console.panel'),\
            patch('foolscap.display.console.curses'):

        test_console = FolioConsole(mock_screen, FAKE_ITEMS)
        with patch.object(test_console, 'key_listener') as mocked_listener:
            mock_position = (0, 1)
            mocked_listener.get_position.return_value = mock_position
            mocked_listener.get_action.side_effect = [
                ('next_tab', 1), ('prev_tab', 1),
                ('next_tab', 1), ('action', 1),
            ]
            mock_display_menu().select_item.return_value = 'selected_note'
            mock_tab().next_tab.side_effect = ['work', 'not_a_book']
            mock_tab().prev_tab.return_value = 'general'

            result = test_console.show()
            assert result == {
                'book': 'work',
                'action': 'list',
                'index': 0,
                'item': 'selected_note'
            }

            result = test_console.show()
            assert result == {
                'book': 'general',
                'action': 'list',
                'index': 0,
                'item': 'selected_note'
            }

            result = test_console.show()
            assert test_console.tabs.next_tab.call_args_list == [call(), call()]
