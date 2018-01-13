import pytest
from mock import MagicMock
from mock import patch

from foolscap.display import key_events

@pytest.mark.parametrize("pos,max_len,expected",
    [(5, 10, 5),
     (11,10, 9),
     (10,10, 9),
     (-1,10, 0)])
def test_check_bounds(pos, max_len, expected):
    result = key_events._check_bounds(pos, max_len)
    assert result == expected


@pytest.mark.parametrize("pos,max_len,expected",
    [(5, 10, 4),
     (9, 10, 8),
     (0, 10, 0)])
def test_move_up(pos, max_len, expected):
    result = key_events._move_up(pos, max_len)
    assert result == expected


@pytest.mark.parametrize("pos,max_len,expected",
    [(5, 10, 6),
     (9, 10, 9),
     (0, 10, 1)])
def test_move_down(pos, max_len, expected):
    result = key_events._move_down(pos, max_len)
    assert result == expected


def test_HandleKeys_init():
    mock_screen = MagicMock()
    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    assert isinstance(test_handler, key_events.HandleKeys)
    assert test_handler.position == 0
    assert test_handler.max_pos == fake_note_count
    assert test_handler.command == None
    assert test_handler.screen == mock_screen


@pytest.mark.parametrize("key_press,expected",
    [('ENTER','view'),
     (ord('e'), 'edit'),
     ('UP_ARROW', None),
     ('DOWN_ARROW', None)])
def test_key_events(key_press, expected):
    mock_screen = MagicMock()
    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    test_handler.position = 5
    with patch("foolscap.display.key_events.ENTER_KEY", ['ENTER']),\
         patch("foolscap.display.key_events.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_events.DOWN_ARROW", 'DOWN_ARROW'):
        mock_screen.getch.return_value = key_press
        assert test_handler.get_action() == expected
        assert test_handler.command == expected
        if key_press == 'UP_ARROW':
            assert test_handler.position == 4
        if key_press == 'DOWN_ARROW':
            assert test_handler.position == 6


def test_key_exit():
    mock_screen = MagicMock()
    mock_screen.getch.return_value = ord('q')
    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    with patch("foolscap.display.key_events.ENTER_KEY", ['ENTER']),\
         patch("foolscap.display.key_events.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_events.DOWN_ARROW", 'DOWN_ARROW'),\
         pytest.raises(SystemExit):
        test_handler.get_action()


def test_get_position():
    mock_screen = MagicMock()
    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    assert test_handler.get_position() == 0
    test_handler.position = 5
    assert test_handler.get_position() == 5

