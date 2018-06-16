import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap.display.render_composite import Widget
from foolscap.display.render_composite import Frame
from foolscap.display.render_composite import HelpBar
from foolscap.display.render_composite import TitleBar
from foolscap.display.render_composite import StatusBar


class FakeWidget(Widget):
    def __init__(self):
        pass
    def draw(self):
        pass

# Test Widget NotImplementedError
# Rewrite the test vocab
def test_Widget_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 90, 110
    test_dis = FakeWidget()
    test_dis.attach_screen(mock_screen)
    assert isinstance(test_dis, Widget)
    assert test_dis.screen == mock_screen
    assert test_dis.top_line == 0
    assert test_dis.max_y == 90
    assert test_dis.max_x == 110
    assert test_dis.bottom_line == 89
    assert test_dis.centre_x == 55


def test_Widget_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 90, 110
    test_dis = FakeWidget()
    test_dis.attach_screen(mock_screen)
    assert test_dis.max_y == 90
    assert test_dis.max_x == 110
    assert test_dis.bottom_line == 89
    assert test_dis.centre_x == 55
    mock_screen.getmaxyx.return_value = 60, 80
    test_dis.update()
    assert test_dis.max_y == 60
    assert test_dis.max_x == 80
    assert test_dis.bottom_line == 59
    assert test_dis.centre_x == 40


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


def test_HelpBar_next_hint():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    mock_help_list = ["HELP", "MORE_HELP"]
    with patch('foolscap.display.render_composite.HELP_OPTIONS', mock_help_list):
        test_bar = HelpBar(mock_screen)
        test_bar.draw()
        test_bar.next_hint()
        test_bar.update()
        test_bar.draw()
        test_bar.next_hint()
        test_bar.update()
        test_bar.draw()

        calls = [
            call(49, 2, "HELP"),
            call(49, 2, "MORE_HELP"),
            # Test it loops back to 0th item
            call(49, 2, "HELP"),
        ]
        mock_screen.addstr.assert_has_calls(calls)


def test_HelpBar_build_help():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    mock_help_list = ["HELP", "MORE_HELP"]
    mock_help_print = "HELP"
    with patch('foolscap.display.render_composite.HELP_OPTIONS', mock_help_list):
        test_bar = HelpBar(mock_screen)
        test_bar.draw()
        mock_screen.addstr.assert_called_with(49, 2, mock_help_print)


def test_HelpBar_build_help_short_width():
    """ Test smaller console where no string can fit in console.
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 6
    mock_help_list = ["HELP", "MORE_HELP"]
    mock_help_print = '--'.join(mock_help_list[:1])
    with patch('foolscap.display.render_composite.HELP_OPTIONS', mock_help_list):
        test_bar = HelpBar(mock_screen)
        test_bar.draw()
        mock_screen.addstr.assert_called_with(49, 2, '')


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


@pytest.mark.parametrize("max_x, expected", [
    (100, "| ~/library/music/good_tunes/tricot |"),
    (90, "| ~/-/music/good_tunes/tricot |"),
    (80, "| ~/-/-/good_tunes/tricot |"),
    (70, "| ~/-/-/-/tricot |"),
    (60, "| tricot |"),
    (40, ""),
])
def test_TitleBar_format_path(max_x, expected):
    separator = 'foolscap.display.render_composite.os.sep'
    test_path = "/home/user/library/music/good_tunes/tricot"

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, max_x

    title_bar = TitleBar(mock_screen)
    with patch(separator, '/'):
        result = title_bar.format_path(test_path)
        assert result == expected


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

