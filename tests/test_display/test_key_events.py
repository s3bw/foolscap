import pytest
from mock import MagicMock
from mock import patch

from foolscap.display import key_events


def test_HandleKeys_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100
    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    assert isinstance(test_handler, key_events.HandleKeys)
    assert test_handler.screen == mock_screen
    assert test_handler.position == 1
    assert test_handler.list_pointer == 0
    assert test_handler.list_top == 0
    assert test_handler.max_pos == fake_note_count
    assert test_handler.command == None
    assert test_handler.top_line == 0
    assert test_handler.max_x == 100
    assert test_handler.max_y == 100
    assert test_handler.bottom_line == 99
    assert test_handler.centre_x == 50


@pytest.mark.parametrize("key_press,expected",
    [('ENTER', ('view', 5)),
     (ord('e'), ('edit', 5)),
     ('UP_ARROW', (None, 4)),
     ('DOWN_ARROW', (None, 6))])
def test_key_events(key_press, expected):
    expected_command, expected_pointer = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    test_handler.position = 5
    test_handler.list_pointer = 5

    with patch("foolscap.display.key_events.ENTER_KEY", ['ENTER']),\
         patch("foolscap.display.key_events.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_events.DOWN_ARROW", 'DOWN_ARROW'):
        mock_screen.getch.return_value = key_press
        assert test_handler.get_action() == expected
        assert test_handler.command == expected_command
        assert test_handler.list_pointer == expected_pointer
        if key_press == 'UP_ARROW':
            assert test_handler.position == 4
        if key_press == 'DOWN_ARROW':
            assert test_handler.position == 6


@pytest.mark.parametrize("pos,max_len,expected",
    [(5, 10, (4, 3)),
     (1, 10, (10, 9)),
     (0, 10, (10, 9))])
def test_cursor_up_movement_large_term(pos, max_len, expected):
    expected_pos, expected_list_index = expected
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 20, 20
    fake_note_count = 10
    test_cursor = key_events.HandleKeys(mock_screen, fake_note_count)
    test_cursor.position = pos
    test_cursor.list_pointer = pos - 1
    test_cursor.move_up()
    assert test_cursor.position == expected_pos
    assert test_cursor.list_pointer == expected_list_index
    assert test_cursor.get_position() == (0, expected_pos)


@pytest.mark.parametrize("pos,max_len,expected",
    # start_pos, notes, end_pos, end_index
     [(5, 10, (6, 5)),
      (9, 10, (10, 9)),
      (10, 10, (1, 0))])
def test_cursor_down_movement_large_term(pos, max_len, expected):
    expected_pos, expected_list_index = expected
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 20, 20
    fake_note_count = 10
    test_cursor = key_events.HandleKeys(mock_screen, fake_note_count)
    test_cursor.position = pos
    test_cursor.list_pointer = pos - 1
    test_cursor.move_down()
    assert test_cursor.position == expected_pos
    assert test_cursor.list_pointer == expected_list_index
    assert test_cursor.get_position() == (0, expected_pos)


@pytest.mark.parametrize("max_len,test_with,expected",
    [(10, (3, 2, 0), (2, 1, 0)),
     (10, (1, 0, 0), (3, 9, 7)),
     (10, (1, 7, 7), (1, 6, 6)),
     (10, (2, 8, 7), (1, 7, 7)),
     (10, (0, 0, 0), (3, 9, 7))])
def test_cursor_up_movement_small_term(max_len, test_with, expected):
    pos, list_pos, list_top = test_with
    expected_pos, expected_list_index, expected_top_note = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 6, 20

    fake_note_count = 10
    test_cursor = key_events.HandleKeys(mock_screen, fake_note_count)
    test_cursor.position = pos
    test_cursor.list_pointer = list_pos
    test_cursor.list_top = list_top
    test_cursor.move_up()

    assert test_cursor.position == expected_pos
    assert test_cursor.list_pointer == expected_list_index
    assert test_cursor.get_position() == (expected_top_note, expected_pos)


@pytest.mark.parametrize("max_len,test_with,expected",
    [(10, (1, 0, 0), (2, 1, 0)),
     (10, (3, 2, 2), (3, 3, 3)),
     (10, (2, 3, 2), (3, 4, 2)),
     (10, (3, 9, 7), (1, 0, 0))])
def test_cursor_down_movement_small_term(max_len, test_with, expected):
    pos, list_pos, list_top = test_with
    expected_pos, expected_list_pos, expected_top_note = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 6, 20

    fake_note_count = 10
    test_cursor = key_events.HandleKeys(mock_screen, fake_note_count)
    test_cursor.position = pos
    test_cursor.list_pointer = list_pos
    test_cursor.list_top = list_top
    test_cursor.move_down()

    assert test_cursor.position == expected_pos
    assert test_cursor.list_pointer == expected_list_pos
    assert test_cursor.get_position() == (expected_top_note, expected_pos)


def test_key_exit():
    mock_screen = MagicMock()
    mock_screen.getch.return_value = ord('q')
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    with patch("foolscap.display.key_events.ENTER_KEY", ['ENTER']),\
         patch("foolscap.display.key_events.UP_ARROW", 'UP_ARROW'),\
         patch("foolscap.display.key_events.DOWN_ARROW", 'DOWN_ARROW'),\
         pytest.raises(SystemExit):
        test_handler.get_action()


def test_get_position():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_note_count = 10
    test_handler = key_events.HandleKeys(mock_screen, fake_note_count)
    assert test_handler.get_position() == (0, 1)
    test_handler.position = 5
    assert test_handler.get_position() == (0, 5)

