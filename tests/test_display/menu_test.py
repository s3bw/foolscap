import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap.display.menu import _set_colour
from foolscap.display.menu import DisplayMenu
from foolscap.display.menu import MenuAdapter

from tests.data.mock_meta_data import FAKE_FOUR_NOTES_W_SUB


# Patch variables:
patch_NORMAL = 'foolscap.display.menu.NORMAL_LINE_COLOUR'
patch_DIM = 'foolscap.display.menu.DIM_LINE_COLOUR'
patch_REVERSE = 'foolscap.display.menu.REVERSE_LINE_COLOUR'

PATCH_COLUMNS = 'foolscap.display.menu_objects.NOTE_CONFIG'
DEFAULT_CONFIG = ['more', 'title', 'description', 'created']


@pytest.mark.parametrize("line,cursor,expected", [
    (3, 4, 'NORMAL'),
    (4, 4, 'REVERSE'),
    (6, 4, 'DIM')
])
def test_set_colour(line, cursor, expected):
    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'):
        result = _set_colour(line, cursor)
        assert result == expected


"""
Setup Notes Model fixture
"""


@pytest.fixture(scope='function')
def display_data():
    from foolscap.meta_data import NotesModel
    from foolscap.note_display import ServiceRules

    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=FAKE_FOUR_NOTES_W_SUB):
        model = NotesModel()
        service_rules = ServiceRules(model)
        items = list(model)
        items = service_rules.order(items)
        items = service_rules.alphabetise(items)
        return service_rules.structure(items)


"""
Test MenuAdapter Object:
"""


def test_MenuAdapter_init(display_data):
    adapter = MenuAdapter(display_data['titles'], display_data['model'])
    assert hasattr(adapter, 'menu')
    assert hasattr(adapter, 'length')
    assert adapter.length == 4


def test_MenuAdapter_iter_viewable(display_data):
    adapter = MenuAdapter(display_data['titles'], display_data['model'])
    result = [n.title for n in adapter.iter_viewable()]
    assert result == ['A', 'B', 'C', 'D']

    for item in adapter.iter_viewable():
        if item.title == 'B':
            item.toggle_drop_down()

    result = [n.title for n in adapter.iter_viewable()]
    assert result == ['A', 'B', '──First Sub:', 'C', 'D']


def test_MenuAdapter_iter_all(display_data):
    adapter = MenuAdapter(display_data['titles'], display_data['model'])
    result = [n.title for n in adapter.iter_all()]
    assert len(result) == 8


"""
Test Display Menu Object:
"""

mock_model = MagicMock()
FAKE_ITEMS = {
    'titles': ["test_title", "another_title"],
    'model': mock_model,
}


def test_DisplayMenu_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(mock_screen, FAKE_ITEMS['titles'], mock_model)

    assert isinstance(test_dm, DisplayMenu)
    assert hasattr(test_dm, 'menu')
    assert hasattr(test_dm, 'columns')
    assert hasattr(test_dm, 'screen')
    assert len(test_dm) == len(FAKE_ITEMS)
    mock_screen.getmaxyx.called_once()


def test_DisplayMenu_update_position():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(
        mock_screen,
        FAKE_ITEMS['titles'],
        mock_model,
    )

    test_dm.update_pointers(1, 3)
    assert hasattr(test_dm, 'cursor')
    assert hasattr(test_dm, 'reduction')
    assert test_dm.cursor == 3
    assert test_dm.reduction == 1


def test_DisplayMenu_expand_item(display_data):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(
        mock_screen,
        display_data['titles'],
        display_data['model'],
    )

    test_dm.expand_item(1)

    result = [n.title for n in test_dm.menu.iter_viewable()]
    assert result == ['A', 'B', '──First Sub:', 'C', 'D']


def test_DisplayMenu_select_item(display_data):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(
        mock_screen,
        display_data['titles'],
        display_data['model']
    )

    result = test_dm.select_item(1)
    assert result == 'B'


def test_DisplayMenu_select_sub_item(display_data):
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(
        mock_screen,
        display_data['titles'],
        display_data['model']
    )

    test_dm.expand_item(1)
    title_result = test_dm.select_item(1)
    subtitle_result = test_dm.select_item(2)
    assert title_result == 'B'
    assert subtitle_result == 'B@1:1'


def test_DisplayMenu_update(display_data):
    """Test that columns are also updated."""
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    with patch('foolscap.display.menu.Columns'):
        test_dm = DisplayMenu(mock_screen, display_data['titles'], mock_model)
        test_dm.update()

        test_dm.columns.update.assert_called_once()


def test_DisplayMenu_draw_item(display_data):
    """Test items are not drawn when they are off the screen."""
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50
    test_dm = DisplayMenu(mock_screen, display_data['titles'], mock_model)
    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'):

        test_dm.update_pointers(2, 3)
        test_dm.draw()

        calls = [
            call.getmaxyx(),
            call.getmaxyx(),
            call.addstr(1, 2, '(+)', 'NORMAL'),
            call.addstr(1, 6, '|', 'NORMAL'),
            call.addstr(1, 8, 'C                    ', 'NORMAL'),
            call.addstr(1, 30, '|', 'NORMAL'),
            call.addstr(2, 2, '(+)', 'DIM'),
            call.addstr(2, 6, '|', 'DIM'),
            call.addstr(2, 8, 'D                    ', 'DIM'),
            call.addstr(2, 30, '|', 'DIM')
        ]

        mock_screen.assert_has_calls(calls)


def test_DisplayMenu_draw():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 100, 100

    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'),\
            patch(PATCH_COLUMNS, DEFAULT_CONFIG):

        test_dm = DisplayMenu(mock_screen, FAKE_ITEMS['titles'], mock_model)
        # Display cursor on note 2.
        test_dm.update_pointers(0, 2)
        test_dm.draw()

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


def test_DisplayMenu_draw_small_height():
    """ Test that note titles are not printed when
        the console height is smaller than the amount
        of notes.
        Params:
            screen max y: 4
            display pointer: 1
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 4, 100

    test_dm = DisplayMenu(mock_screen, FAKE_ITEMS['titles'], mock_model)
    test_dm.update_pointers(0, 1)

    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'):
        test_dm.draw()
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


def test_DisplayMenu_draw_small_width():
    """ Test that note descriptions are not printed
        when the width of the console is too small.
        Params:
            screen max x: 50
            display pointer: 2
    """
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 50, 50

    test_dm = DisplayMenu(mock_screen, FAKE_ITEMS['titles'], mock_model)
    test_dm.update_pointers(0, 2)

    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'):
        test_dm.draw()
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


def test_DisplayMenu_draw_smaller():
    fake_items = [
        "test_title",
        "another_title_1",
        "another_title_2",
        "another_title_3",
        "another_title_4",
        "another_title_5",
    ]
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 7, 50

    test_dm = DisplayMenu(mock_screen, fake_items, mock_model)
    test_dm.update_pointers(0, 2)

    with patch(patch_NORMAL, 'NORMAL'),\
            patch(patch_DIM, 'DIM'),\
            patch(patch_REVERSE, 'REVERSE'):
        test_dm.draw()
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

