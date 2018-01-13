import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap.display.content_display import _set_colour
from foolscap.display.content_display import DisplayContents


# Patch variables:
patch_NORMAL = 'foolscap.display.content_display.NORMAL_LINE_COLOUR'
patch_DIM = 'foolscap.display.content_display.DIM_LINE_COLOUR'
patch_REVERSE = 'foolscap.display.content_display.REVERSE_LINE_COLOUR'
patch_TITLE = 'foolscap.display.content_display.TITLE'
patch_DESCRIP = 'foolscap.display.content_display.DESCRIPTION'

FAKE_ITEMS = [
    ("test_title", "test description"),
    ("another_title", "another description"),
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
    test_DC = DisplayContents(mock_screen, FAKE_ITEMS)

    assert isinstance(test_DC, DisplayContents)
    assert hasattr(test_DC, 'items')
    assert test_DC.items == FAKE_ITEMS
    mock_screen.getmaxyx.called_once()


def test_DisplayContents_update_position():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_DC = DisplayContents(mock_screen, FAKE_ITEMS)

    test_DC.update_position(3)
    assert hasattr(test_DC, 'position')
    assert test_DC.position == 3


def test_DisplayContents_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    test_DC = DisplayContents(mock_screen, FAKE_ITEMS)
    test_DC.update_position(1)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'),\
         patch(patch_TITLE, '{}'),\
         patch(patch_DESCRIP, '{}'):
        test_DC.draw()
        calls = [call.getmaxyx(),
                 call.addstr(1, 0, "test_title", "DIM"),
                 call.addstr(1, 50, "test description", "DIM"),
                 call.addstr(2, 0, "another_title", "REVERSE"),
                 call.addstr(2, 50, "another description", "REVERSE")]
        mock_screen.assert_has_calls(calls)


def test_DisplayContents_draw_small():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50

    test_DC = DisplayContents(mock_screen, FAKE_ITEMS)
    test_DC.update_position(1)

    with patch(patch_NORMAL, 'NORMAL'),\
         patch(patch_DIM, 'DIM'),\
         patch(patch_REVERSE, 'REVERSE'),\
         patch(patch_TITLE, '{}'),\
         patch(patch_DESCRIP, '{}'):
        test_DC.draw()
        calls = [call.getmaxyx(),
                 call.addstr(1, 0, "test_title", "DIM"),
                 call.addstr(2, 0, "another_title", "REVERSE")]
        mock_screen.assert_has_calls(calls)


