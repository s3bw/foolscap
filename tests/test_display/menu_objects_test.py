from foolscap.display.menu_objects import MenuItem


def test_MenuItem_init():
    mock_model = {'description': 'that'}
    mock_item = {'title': 'This', 'model': mock_model}
    item = MenuItem(**mock_item)
    assert item.title == 'This'
    assert item.description == 'that'
    assert not hasattr(item, 'sub_headings')
    assert not hasattr(item, 'expand')


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
        assert expected[1] in result.description


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
