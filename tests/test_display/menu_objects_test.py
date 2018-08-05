from datetime import datetime

import pytest
from mock import patch

from foolscap.display.menu_objects import MenuItem
from foolscap.display.menu_objects import ColumnType
from foolscap.display.menu_objects import ColumnRegistry
from foolscap.display.menu_objects import display_text
from foolscap.display.menu_objects import Columns

from tests.data.mock_meta_data import FAKE_FOUR_NOTES_W_SUB


"""
Setup Test Fixtures:
"""

@pytest.fixture(scope='function')
def model_items():
    from foolscap.meta_data import NotesModel
    from foolscap.note_display import Controller
    from foolscap.note_display import ServiceRules

    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=FAKE_FOUR_NOTES_W_SUB):
        model = NotesModel()
        service_rules = ServiceRules(model)
        items = list(model)
        items = service_rules.order(items)
        items = service_rules.alphabetise(items)
        return service_rules.structure(items)


@pytest.fixture(scope='function')
def tag_items():
    from foolscap.meta_data import NotesModel
    from foolscap.meta_data import TagsModel
    from foolscap.note_display import Controller
    from foolscap.note_display import ServiceRules

    patch_load = 'foolscap.meta_data.models.load_meta'
    with patch(patch_load, return_value=FAKE_FOUR_NOTES_W_SUB):
        model = NotesModel()
        model = TagsModel(model)
        service_rules = ServiceRules(model)
        items = list(model)
        items = service_rules.order(items)
        items = service_rules.alphabetise(items)
        return service_rules.structure(items)

"""
Test the Column Prototype:
"""


def test_ColumnType():
    prototype = ColumnType()

    type_1 = {'a': 'this'}
    type_2 = {'b': 'that'}

    item_1 = prototype.clone(**type_1)
    item_2 = prototype.clone(**type_2)

    assert hasattr(item_1, 'a')
    assert item_1.a == 'this'

    assert hasattr(item_2, 'b')
    assert item_2.b == 'that'

    assert not hasattr(item_1, 'b')
    assert not hasattr(item_2, 'a')


"""
Test the Column Registry:
"""


def test_ColumnRegistry():
    prototype = ColumnType()
    type_1 = {'name': 'object_a'}
    item_1 = prototype.clone(**type_1)
    type_2 = {'name': 'object_b'}
    item_2 = prototype.clone(**type_2)

    registry = ColumnRegistry()

    assert hasattr(registry, '_objects')
    registry.register_object(item_1.name, item_1)
    registry.register_object(item_2.name, item_2)

    assert item_1 is registry.get_object('object_a')
    registry.unregister_object('object_a')
    assert ['object_b'] == list(registry.get_objects())


@pytest.mark.parametrize("_input, expected", [
    (datetime(2013, 1, 2), "02-Jan-2013"),
    (15, "15"),
    ("get", "get")
])
def test_display_text(_input, expected):
    result = display_text(_input)
    assert result == expected


"""
Test Columns Object:
"""


def test_Columns_init():
    from foolscap.display.menu_objects import NOTE_CONFIG
    from foolscap.display.menu_objects import TAG_SETTINGS
    from foolscap.display.menu_objects import DEFAULT_SETTINGS

    columns = Columns('notes')
    assert hasattr(columns, 'settings')
    assert hasattr(columns, 'configuration')
    assert hasattr(columns, 'registry')
    assert columns.settings == DEFAULT_SETTINGS
    assert columns.configuration == NOTE_CONFIG
    assert len(list(columns.registry.get_objects())) == len(NOTE_CONFIG)

    columns = Columns('tags')
    assert columns.settings == TAG_SETTINGS
    assert columns.configuration == ['more', 'title', 'description']


@pytest.mark.parametrize("input_text, size, expected", [
    ("item", 2, "it "),
    ("item", 5, "item  "),
    ("item", 6, "item   "),
    ("item", 7, "item    "),
    ("it", 7, "it      "),
    ("item", 8, "item     "),
])
def test_Columns_left_align(input_text, size, expected):
    columns = Columns('notes')
    result = columns.left_align(input_text, size)
    assert result == expected


@pytest.mark.parametrize("input_text, size, expected", [
    ("item", 5, " item "),
    ("item", 6, " item "),
    ("item", 7, "  item  "),
    ("it", 7, "   it   "),
    ("item", 8, "  item  "),
])
def test_Columns_centre_align(input_text, size, expected):
    columns = Columns('notes')
    result = columns.centre_align(input_text, size)
    assert result == expected


def test_Columns_draw():
    """Tested in Display Menu."""
    pass


"""
Test Menu Items:
"""


def test_MenuItem_init():
    mock_model = {'description': 'that'}
    mock_item = {'title': 'This', 'model': mock_model}
    item = MenuItem(**mock_item)
    assert item.title == 'This'
    assert item.raw_title == 'This'
    assert item.description == 'that'
    assert not hasattr(item, 'sub_headings')
    assert not hasattr(item, 'expand')


def test_MenuItem_NotesModel_init(model_items):
    item = MenuItem(**model_items[0])
    assert item.title == 'A'


def test_MenuItem_TagModel_init(tag_items):
    item = MenuItem(**tag_items[0])
    assert item.title == 'fake_tag'
    assert item.raw_title == 'fake_tag'


def test_MenuItem_init_sub():
    mock_sub = [('1sub', 'desc', 2, 5), ('2sub', 'desc', 6, 10)]
    mock_model = {'description': 'that', 'sub_headings': mock_sub}
    mock_item = {'title': 'This', 'model': mock_model}
    item = MenuItem(**mock_item)
    assert item.title == 'This'
    assert item.description == 'that'
    assert hasattr(item, 'sub_items')
    assert hasattr(item, 'expand')
    assert len(item.sub_items) == 2
    for result, expected in zip(item.sub_items, mock_sub):
        assert isinstance(result, MenuItem)
        assert expected[0] in result.title
        assert expected[0] in result.raw_title
        assert expected[1] in result.description
        assert result.parent_title == item.title


def test_MenuItem_toggle():
    mock_sub = [('1sub', 'desc', 2, 5), ('2sub', 'desc', 6, 10)]
    mock_model = {'description': 'that', 'sub_headings': mock_sub}
    mock_item = {'title': 'This', 'model': mock_model}
    item = MenuItem(**mock_item)
    assert item.expand == False
    item.toggle_drop_down()
    assert item.expand == True
    item.toggle_drop_down()
    assert item.expand == False
