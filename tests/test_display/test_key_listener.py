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
    assert test_listener.command == None
    assert test_listener.scroll


def test_KeyListener_setmax():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    test_listener.set_max(20)
    assert test_listener.max_pos == 20


@pytest.mark.parametrize("key_press, expected",
    [('ENTER', ('view', 5, None)),
     (ord('e'), ('edit', 5, None)),
     (ord('X'), ('export', 5, None)),
     (ord('g'), (None, 1, None)),
     (ord('G'), (None, 9, None)),
     ('UP_ARROW', (None, 4, None)),
     ('DOWN_ARROW', (None, 6, None)),
     ('RIGHT_ARROW', (None, 5, 5))])
def test_key_listener(key_press, expected):
    expected_command, expected_pointer, expected_expand = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_listener = key_listener.KeyListener(mock_screen, fake_note_count)
    test_listener.scroll.position = 5
    test_listener.scroll.list_pointer = 5

    with patch("foolscap.display.key_listener.ENTER_KEY", ['ENTER']),\
         patch("foolscap.display.key_listener.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_listener.DOWN_ARROW", 'DOWN_ARROW'),\
         patch("foolscap.display.key_listener.RIGHT_ARROW", 'RIGHT_ARROW'):
        mock_screen.getch.return_value = key_press
        assert test_listener.get_action() == expected
        assert test_listener.command == expected_command
        assert test_listener.scroll.list_pointer == expected_pointer
        if key_press == 'UP_ARROW':
            assert test_listener.scroll.position == 4
        if key_press == 'DOWN_ARROW':
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
         patch("foolscap.display.key_listener.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_listener.DOWN_ARROW", 'DOWN_ARROW'),\
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
    mock_screen.getch.return_value = 'UP_ARROW'

    fake_note_count = 20
    tail_index = 19
    top_note = 8
    cursor_pos = 12
    with patch("foolscap.display.key_listener.UP_ARROW", 'UP_ARROW'):
        test_listener = key_listener.KeyListener(mock_screen, fake_note_count)

        assert test_listener.get_position() == (0, 1)
        result = test_listener.get_action()
        assert result == (None, tail_index, None)
        assert test_listener.get_position() == (top_note, cursor_pos)

