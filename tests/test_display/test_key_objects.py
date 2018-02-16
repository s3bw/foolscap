import pytest
from mock import MagicMock
from mock import patch

from foolscap.display import key_objects


def test_Scrollable_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_max_pos = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_max_pos)

    assert isinstance(test_scroll, key_objects.Scrollable)
    assert test_scroll.screen == mock_screen
    assert test_scroll.position == 1
    assert test_scroll.list_pointer == 0
    assert test_scroll.list_top == 0
    assert test_scroll.max_pos == fake_max_pos

    assert test_scroll.max_x == 100
    assert test_scroll.max_y == 100
    assert test_scroll.bottom_line == 99
    assert test_scroll.centre_x == 50


def test_Scrollable_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    fake_max_pos = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_max_pos)

    test_scroll.update(20)
    assert test_scroll.max_pos == 20


@pytest.mark.parametrize("pos, max_len, expected",
    [(5, 10, (4, 3)),
     (1, 10, (10, 9)),
     (0, 10, (10, 9))])
def test_scroll_up_movement_large_term(pos, max_len, expected):
    expected_pos, expected_list_index = expected
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 20, 20
    fake_note_count = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_note_count)
    test_scroll.position = pos
    test_scroll.list_pointer = pos - 1
    test_scroll.move_up()
    assert test_scroll.position == expected_pos
    assert test_scroll.list_pointer == expected_list_index
    assert test_scroll.list_top == 0


@pytest.mark.parametrize("pos, max_len, expected",
    # start_pos, notes, end_pos, end_index
     [(5, 10, (6, 5)),
      (9, 10, (10, 9)),
      (10, 10, (1, 0))])
def test_scroll_down_movement_large_term(pos, max_len, expected):
    expected_pos, expected_list_index = expected
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 20, 20
    fake_note_count = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_note_count)
    test_scroll.position = pos
    test_scroll.list_pointer = pos - 1
    test_scroll.move_down()
    assert test_scroll.position == expected_pos
    assert test_scroll.list_pointer == expected_list_index
    assert test_scroll.list_top == 0


@pytest.mark.parametrize("max_len, test_with, expected",
    [(10, (3, 2, 0), (2, 1, 0)),
     (10, (1, 0, 0), (3, 9, 7)),
     (10, (1, 7, 7), (1, 6, 6)),
     (10, (2, 8, 7), (1, 7, 7)),
     (10, (0, 0, 0), (3, 9, 7))])
def test_scroll_up_movement_small_term(max_len, test_with, expected):
    pos, list_pos, list_top = test_with
    expected_pos, expected_list_index, expected_list_top = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 6, 20

    fake_note_count = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_note_count)
    test_scroll.position = pos
    test_scroll.list_pointer = list_pos
    test_scroll.list_top = list_top
    test_scroll.move_up()

    assert test_scroll.position == expected_pos
    assert test_scroll.list_pointer == expected_list_index
    assert test_scroll.list_top == expected_list_top


@pytest.mark.parametrize("max_len, test_with, expected",
    [(10, (1, 0, 0), (2, 1, 0)),
     (10, (3, 2, 2), (3, 3, 3)),
     (10, (2, 3, 2), (3, 4, 2)),
     (10, (3, 9, 7), (1, 0, 0))])
def test_scroll_down_movement_small_term(max_len, test_with, expected):
    pos, list_pos, list_top = test_with
    expected_pos, expected_list_pos, expected_list_top = expected

    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 6, 20

    fake_note_count = 10
    test_scroll = key_objects.Scrollable(mock_screen, fake_note_count)
    test_scroll.position = pos
    test_scroll.list_pointer = list_pos
    test_scroll.list_top = list_top
    test_scroll.move_down()

    assert test_scroll.position == expected_pos
    assert test_scroll.list_pointer == expected_list_pos
    assert test_scroll.list_top == expected_list_top

