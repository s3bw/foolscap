import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap.display.menu import _set_colour
from foolscap.display.menu import DisplayMenu


# Patch variables:
patch_NORMAL = 'foolscap.display.menu.NORMAL_LINE_COLOUR'
patch_DIM = 'foolscap.display.menu.DIM_LINE_COLOUR'
patch_REVERSE = 'foolscap.display.menu.REVERSE_LINE_COLOUR'

mock_model = MagicMock()
FAKE_ITEMS = [
    {
        'title': "test_title",
        'description': "test description",
        'model': mock_model,
    },
    {
        'title': "another_title",
        'description': "another description",
        'model': mock_model,
    },
]


@pytest.mark.parametrize("line,cursor,expected",
    [(3,4,'NORMAL'),
     (4,4,'REVERSE'),
     (6,4,'DIM')])
def test_set_colour(line, cursor, expected):
    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'):
        result = _set_colour(line, cursor)
        assert result == expected


def test_DisplayContents_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_DC = DisplayMenu(mock_screen, FAKE_ITEMS)

    assert isinstance(test_DC, DisplayMenu)
    assert hasattr(test_DC, 'menu')
    assert len(test_DC) == len(FAKE_ITEMS)
    mock_screen.getmaxyx.called_once()


def test_DisplayContents_update_position():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_DC = DisplayMenu(mock_screen, FAKE_ITEMS)

    test_DC.update_pointers(1, 3)
    assert hasattr(test_DC, 'cursor')
    assert hasattr(test_DC, 'reduction')
    assert test_DC.cursor == 3
    assert test_DC.reduction == 1


def test_DisplayContents_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    test_DC = DisplayMenu(mock_screen, FAKE_ITEMS)
    # Display cursor on note 2.
    test_DC.update_pointers(0, 2)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'):
        test_DC.draw()

        calls = [
            call.getmaxyx(),
            call.getmaxyx(),
            call.addstr(1, 2, '(+)', 'NORMAL'),
            call.addstr(1, 6, '|', 'NORMAL'),
            call.addstr(1, 8, 'test_title           ', 'NORMAL'),
            call.addstr(1, 30, '|', 'NORMAL'),
            call.addstr(1, 32, '-                                        ', 'NORMAL'),
            call.addstr(1, 74, '|', 'NORMAL'),
            call.addstr(1, 76, '     -     ', 'NORMAL'),
            call.addstr(1, 88, '|', 'NORMAL'),
            call.addstr(2, 2, '(+)', 'REVERSE'),
            call.addstr(2, 6, '|', 'REVERSE'),
            call.addstr(2, 8, 'another_title        ', 'REVERSE'),
            call.addstr(2, 30, '|', 'REVERSE'),
            call.addstr(2, 32, '-                                        ', 'REVERSE'),
            call.addstr(2, 74, '|', 'REVERSE'),
            call.addstr(2, 76, '     -     ', 'REVERSE'),
            call.addstr(2, 88, '|', 'REVERSE')]

        mock_screen.assert_has_calls(calls)


def test_DisplayContents_draw_small_height():
    """ Test that note titles are not printed when
        the console height is smaller than the amount
        of notes.
        Params:
            screen max y: 4
            display pointer: 1
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 4, 100

    test_DC = DisplayMenu(mock_screen, FAKE_ITEMS)
    test_DC.update_pointers(0, 1)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'):
        test_DC.draw()
        calls = [
            call.getmaxyx(),
            call.getmaxyx(),
            call.addstr(1, 2, '(+)', 'REVERSE'),
            call.addstr(1, 6, '|', 'REVERSE'),
            call.addstr(1, 8, 'test_title           ', 'REVERSE'),
            call.addstr(1, 30, '|', 'REVERSE'),
            call.addstr(1, 32, '-                                        ', 'REVERSE'),
            call.addstr(1, 74, '|', 'REVERSE'),
            call.addstr(1, 76, '     -     ', 'REVERSE'),
            call.addstr(1, 88, '|', 'REVERSE')]

        mock_screen.assert_has_calls(calls)



def test_DisplayContents_draw_small_width():
    """ Test that note descriptions are not printed
        when the width of the console is too small.
        Params:
            screen max x: 50
            display pointer: 2
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50

    test_DC = DisplayMenu(mock_screen, FAKE_ITEMS)
    test_DC.update_pointers(0, 2)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'):
        test_DC.draw()
        calls = [
            call.getmaxyx(),
            call.getmaxyx(),
            call.addstr(1, 2, '(+)', 'NORMAL'),
            call.addstr(1, 6, '|', 'NORMAL'),
            call.addstr(1, 8, 'test_title           ', 'NORMAL'),
            call.addstr(1, 30, '|', 'NORMAL'),
            call.addstr(2, 2, '(+)', 'REVERSE'),
            call.addstr(2, 6, '|', 'REVERSE'),
            call.addstr(2, 8, 'another_title        ', 'REVERSE'),
            call.addstr(2, 30, '|', 'REVERSE')]
        mock_screen.assert_has_calls(calls)


def test_DisplayContents_draw_smaller():
    fake_items = [
        {'title': "test_title", 'description': "test description",
        'model': mock_model},
        {'title': "another_title_1", 'description': "another description",
        'model': mock_model},
        {'title': "another_title_2", 'description': "another description",
        'model': mock_model},
        {'title': "another_title_3", 'description': "another description",
        'model': mock_model},
        {'title': "another_title_4", 'description': "another description",
        'model': mock_model},
        {'title': "another_title_5", 'description': "another description",
        'model': mock_model},
    ]
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 7, 50

    test_DC = DisplayMenu(mock_screen, fake_items)
    test_DC.update_pointers(0, 2)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'):
        test_DC.draw()
        calls = [
            call.getmaxyx(),
            call.getmaxyx(),
            call.addstr(1, 2, '(+)', 'NORMAL'),
            call.addstr(1, 6, '|', 'NORMAL'),
            call.addstr(1, 8, 'test_title           ', 'NORMAL'),
            call.addstr(1, 30, '|', 'NORMAL'),
            call.addstr(2, 2, '(+)', 'REVERSE'),
            call.addstr(2, 6, '|', 'REVERSE'),
            call.addstr(2, 8, 'another_title_1      ', 'REVERSE'),
            call.addstr(2, 30, '|', 'REVERSE'),
            call.addstr(3, 2, '(+)', 'NORMAL'),
            call.addstr(3, 6, '|', 'NORMAL'),
            call.addstr(3, 8, 'another_title_2      ', 'NORMAL'),
            call.addstr(3, 30, '|', 'NORMAL'),
            call.addstr(4, 2, '(+)', 'DIM'),
            call.addstr(4, 6, '|', 'DIM'),
            call.addstr(4, 8, 'another_title_3      ', 'DIM'),
            call.addstr(4, 30, '|', 'DIM')]

        mock_screen.assert_has_calls(calls)


