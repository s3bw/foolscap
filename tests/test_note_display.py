import pytest
from mock import patch

import foolscap.note_display as note_display

from data.test_meta_data import FAKE_SINGLE_NOTE
from data.test_meta_data import FAKE_MANY_NOTES


# Little reminder on how to use parametrize:
@pytest.mark.parametrize("expected",[1,2])
def test_param(expected):
    assert expected / 3 < 1


@pytest.mark.parametrize("inp,expected",
    [(1,2),
     (2,4)])
def test_param(inp, expected):
    result = inp * 2
    assert result == expected


@pytest.mark.parametrize("test_dict,expected",[ 
    (FAKE_MANY_NOTES.copy(),[
        ('recently_opened', 'This is a fake note'),
        ('most_viewed', 'This is a fake note'),
        ('second_most', 'This is a fake note'),
        ('third_most', 'This is a fake note'),
        ('A', 'This is a fake note'),
        ('fake_note_1', 'This is a fake note'),
        ('Z', 'This is a fake note'),
        ]),
    (FAKE_SINGLE_NOTE.copy(),[
        ('most_viewed', 'This is a fake note'),
        ])
    ])
# No tag filtering
def test_list_notes(test_dict, expected):
    def fake_return(input_param):
        return input_param

    with patch('foolscap.note_display.display_list') as mock_display:
        mock_display.side_effect = fake_return
        result = note_display.list_notes(None, test_dict)
        assert result == expected


def test_list_notes_with_no_tag_matches():
    test_dict = FAKE_MANY_NOTES.copy()
    with pytest.raises(SystemExit):
        note_display.list_notes('no_match_tag', test_dict)


@pytest.mark.parametrize("sorted_list,test_dict,expected",[
    (
        ['A','second_most','fake_note_1'],
        FAKE_MANY_NOTES.copy(),
        [
            ('A', 'This is a fake note'),
            ('second_most', 'This is a fake note'),
            ('fake_note_1', 'This is a fake note'),
        ]
    ),
    (
        ['most_viewed'],
        FAKE_SINGLE_NOTE.copy(),
        [
            ('most_viewed', 'This is a fake note')
        ]
    )])
def test_display_information(sorted_list, test_dict, expected):
    result = note_display.display_information(sorted_list, test_dict)
    assert result == expected


@pytest.mark.parametrize("test_dict,expected",[
    (FAKE_MANY_NOTES.copy(),'most_viewed'),
    (FAKE_SINGLE_NOTE.copy(), 'most_viewed')
    ])
def test_most_views_pop(test_dict, expected):
   result = note_display.most_views_pop(test_dict)
   assert result == expected


@pytest.mark.parametrize("test_dict,expected",[
    (FAKE_MANY_NOTES.copy(),['most_viewed',
                             'second_most',
                             'third_most']),
    (FAKE_SINGLE_NOTE.copy(),['most_viewed',
                               None,
                               None])
    ])
def test_most_views_pop_range(test_dict, expected):
    for n in range(3):
        result = note_display.most_views_pop(test_dict)
        assert result == expected[n]


@pytest.mark.parametrize("test_dict,expected",[
    (FAKE_MANY_NOTES.copy(),'recently_opened'),
    ({}, None)
    ])
def test_find_last_opened(test_dict, expected):
    result = note_display.find_last_opened(test_dict)
    assert result == expected


@pytest.mark.parametrize("test_dict,expected",[ 
    (FAKE_MANY_NOTES.copy(),[
        'recently_opened',
        'most_viewed',
        'second_most',
        'third_most',
        'A',
        'fake_note_1',
        'Z',
        ]),
    (FAKE_SINGLE_NOTE.copy(),[
        'most_viewed'
        ])
    ])
def test_sort_notes(test_dict, expected):
    result = note_display.sort_notes(test_dict)
    assert result == expected
    




