import pytest
from mock import call
from mock import MagicMock

from foolscap.display.render_objects import Frame
from foolscap.display.render_objects import HelpBar
from foolscap.display.render_objects import TitleBar
from foolscap.display.render_objects import StatusBar


def test_Frame_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_frame = Frame(mock_screen)
    assert isinstance(test_frame, Frame)
    assert mock_screen.getmaxyx.called_once()


def test_Frame_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_frame = Frame(mock_screen)
    test_frame.draw()
    mock_screen.border.assert_called_with('|', '|', '-', '-', '+', '+', '+', '+')


def test_Frame_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_frame = Frame(mock_screen)
    assert mock_screen.getmaxyx.called_once()
    test_frame.update()


def test_HelpBar_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_bar = HelpBar(mock_screen)
    assert isinstance(test_bar, HelpBar)
    assert mock_screen.getmaxyx.called_once()
    assert hasattr(test_bar, 'help_string')


def test_HelpBar_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    mock_help_string = "HELP"
    test_bar = HelpBar(mock_screen)
    test_bar.help_string = mock_help_string
    test_bar.draw()
    mock_screen.addstr.assert_called_with(49, 2, mock_help_string)


def test_HelpBar_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_bar = HelpBar(mock_screen)
    assert mock_screen.getmaxyx.called_once()
    test_bar.update()


def test_TitleBar_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_title_bar = TitleBar(mock_screen)
    assert isinstance(test_title_bar, TitleBar)
    assert mock_screen.getmaxyx.called_once()
    assert hasattr(test_title_bar, 'heading')
    assert hasattr(test_title_bar, 'cwd')


def test_TitleBar_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    mock_heading = "HEADER"
    mock_path = "PATH"
    test_title_bar = TitleBar(mock_screen)
    test_title_bar.heading = mock_heading
    test_title_bar.cwd = mock_path
    test_title_bar.centre_header = 22
    test_title_bar.draw()
    calls = [call(0, 22, mock_heading), call(0, 42, mock_path)]
    assert mock_screen.addstr.call_args_list == calls


def test_TitleBar_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    mock_heading = "HEADER"
    test_title_bar = TitleBar(mock_screen)
    test_title_bar.heading = mock_heading
    assert mock_screen.getmaxyx.called_once()
    test_title_bar.update()
    assert test_title_bar.centre_header == 22


def test_StatusBar_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_status = StatusBar(mock_screen, 10)
    assert isinstance(test_status, StatusBar)
    assert mock_screen.getmaxyx.called_once()
    assert hasattr(test_status, 'display_text')
    assert test_status.display_text == "Notes: 10"


def test_StatusBar_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50

    mock_display = "Notes: 10"
    test_status = StatusBar(mock_screen, 10)
    test_status.display_text = mock_display
    test_status.draw()
    mock_screen.addstr.assert_called_with(48, 2, mock_display)


def test_StatusBar_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_status = StatusBar(mock_screen, 10)
    assert mock_screen.getmaxyx.called_once()
    test_status.update()

