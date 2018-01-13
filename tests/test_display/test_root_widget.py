from mock import MagicMock

from foolscap.display import root_widget


def test_Displayable_init():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 90, 110
    test_dis = root_widget.Displayable(mock_screen)
    assert isinstance(test_dis, root_widget.Displayable)
    assert test_dis.screen == mock_screen
    assert test_dis.top_line == 0
    assert test_dis.max_y == 90
    assert test_dis.max_x == 110
    assert test_dis.bottom_line == 89
    assert test_dis.centre_x == 55


def test_Displayable_update():
    mock_screen = MagicMock()
    mock_screen.getmaxyx.return_value = 90, 110
    test_dis = root_widget.Displayable(mock_screen)
    assert test_dis.max_y == 90
    assert test_dis.max_x == 110
    assert test_dis.bottom_line == 89
    assert test_dis.centre_x == 55
    mock_screen.getmaxyx.return_value = 60, 80
    test_dis.update()
    assert test_dis.max_y == 60
    assert test_dis.max_x == 80
    assert test_dis.bottom_line == 59
    assert test_dis.centre_x == 40
    

