from foolscap.display.content import MenuItem
from foolscap.display.content import SubItem


def test_MenuItem_init():
    item = MenuItem('Title', 'Description', None)
    assert item.title == 'Title'
    assert item.desc == 'Description'
    assert not hasattr(item, 'sub_items')
    assert not hasattr(item, 'expand')


def test_MenuItem_init_sub():
    mock_sub = [('1sub', 'desc'), ('2sub', 'desc')]
    item = MenuItem('Title', 'Description', mock_sub)
    assert item.title == 'Title'
    assert item.desc == 'Description'
    assert hasattr(item, 'sub_items')
    assert hasattr(item, 'expand')
    assert len(item.sub_items) == 2
    for result, expected in zip(item.sub_items, mock_sub):
        assert isinstance(result, SubItem)
        assert result.title == expected[0]
        assert result.desc == expected[1]


def test_MenuItem_toggle():
    mock_sub = [('1sub', 'desc'), ('2sub', 'desc')]
    item = MenuItem('Title', 'Description', mock_sub)
    assert item.expand == False
    item.toggle_drop_down()
    assert item.expand == True
    item.toggle_drop_down()
    assert item.expand == False
