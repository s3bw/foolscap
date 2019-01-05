import pytest
from mock import MagicMock
from mock import patch

from foolscap.display import key_listener


def test_KeyListener_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    assert isinstance(test_listener, key_listener.KeyListener)
    assert test_listener.screen == mock_screen
    assert test_listener.max_pos == fake_note_count
    assert test_listener.command is None
    assert test_listener.scroll


def test_KeyListener_setmax():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    test_listener.set_max(20)
    assert test_listener.max_pos == 20


@pytest.mark.parametrize("key_press, expected", [
    ('ENTER', ('view', 5)),
    (ord('i'), ('edit', 5)),
    (ord('X'), ('export', 5)),
    (ord('H'), ('help', 5)),
    (ord('g'), (None, 1)),
    (ord('G'), (None, 9)),
    (ord('l'), ('next_tab', 5)),
    (ord('h'), ('prev_tab', 5)),
    (ord('k'), (None, 4)),
    (ord('j'), (None, 6)),
    (ord('e'), ('expand', 5))
])
def test_key_listener(key_press, expected):
    expected_command, expected_pointer = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    test_listener.scroll.position = 5
    test_listener.scroll.list_pointer = 5

    with patch("foolscap.display.key_listener.ENTER_KEY", ['ENTER']):
        mock_screen.getch.return_value = key_press
        assert test_listener.get_action() == expected
        assert test_listener.command == expected_command
        assert test_listener.scroll.list_pointer == expected_pointer
        if key_press == ord('k'):
            assert test_listener.scroll.position == 4
        if key_press == ord('j'):
            assert test_listener.scroll.position == 6
        if key_press == ord('g'):
            assert test_listener.scroll.position == 1
        if key_press == ord('G'):
            assert test_listener.scroll.position == 10


def test_key_exit():
    mock_screen = MagicMock()
    mock_screen.getch.return_value = ord('q')
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    with patch("foolscap.display.key_listener.ENTER_KEY", ['ENTER']),\
            pytest.raises(SystemExit):
        test_listener.get_action()


def test_get_position():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    assert test_listener.get_position() == (0, 1)
    test_listener.scroll.position = 5
    assert test_listener.get_position() == (0, 5)


def test_get_position_small():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 15, 100
    mock_screen.getch.return_value = ord('k')

    fake_note_count = 20
    tail_index = 19
    top_note = 8
    cursor_pos = 12
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)

    assert test_listener.get_position() == (0, 1)
    result = test_listener.get_action()
    assert result == (None, tail_index)
    assert test_listener.get_position() == (top_note, cursor_pos)

