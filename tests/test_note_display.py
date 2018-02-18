import pytest
from mock import patch

import foolscap.note_display as note_display

from data.mock_meta_data import FAKE_SINGLE_NOTE
from data.mock_meta_data import FAKE_SINGLE_NOTE_2
from data.mock_meta_data import FAKE_MANY_NOTES
from data.mock_meta_data import FAKE_NOTES_EDGE_CASE
from data.mock_meta_data import FOUR_FAKE_NOTES


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
        {'title': 'recently_opened', 'description': 'This is a fake note'},
        {'title': 'most_viewed', 'description': 'This is a fake note'},
        {'title': 'second_most', 'description': 'This is a fake note'},
        {'title': 'third_most', 'description': 'This is a fake note'},
        {'title': 'A', 'description': 'This is a fake note'},
        {'title': 'fake_note_1', 'description': 'This is a fake note'},
        {'title': 'Z', 'description': 'This is a fake note'},
        ]),
    (FAKE_SINGLE_NOTE.copy(),[
        {'title': 'most_viewed', 'description': 'This is a fake note'},
        ])
    ])
# No tag filtering
def test_list_notes(test_dict, expected):
    def fake_return(input_param):
        return input_param

    with patch('foolscap.note_display.display_list') as mock_display,\
         patch('foolscap.note_display.load_meta') as mock_meta:
        mock_meta.return_value = test_dict
        mock_display.side_effect = fake_return
        result = note_display.list_notes(None)
        assert result == expected


def test_list_notes_with_no_tag_matches():
    with pytest.raises(SystemExit):
        note_display.list_notes('no_match_tag')


@pytest.mark.parametrize("sorted_list,test_dict,expected",[
    (
        ['A','second_most','fake_note_1'],
        FAKE_MANY_NOTES.copy(),
        [
            {'title': 'A', 'description': 'This is a fake note'},
            {'title': 'second_most', 'description': 'This is a fake note'},
            {'title': 'fake_note_1', 'description': 'This is a fake note'},
        ]
    ),
    (
        ['most_viewed'],
        FAKE_SINGLE_NOTE.copy(),
        [
            {'title': 'most_viewed', 'description': 'This is a fake note'}
        ]
    ),
    (
        ['most_viewed'],
        FAKE_SINGLE_NOTE_2.copy(),
        [
            {'title': 'most_viewed', 
             'description': 'This is a fake note',
             'sub_headings': [('First Sub:', ':A sub headings')]},
        ]
    )])
def test_display_information(sorted_list, test_dict, expected):
    result = note_display.display_information(sorted_list, test_dict)
    assert result == expected


@pytest.mark.parametrize("test_dict, expected",[
    (FAKE_MANY_NOTES.copy(),['most_viewed', 'second_most', 'third_most']),
    (FOUR_FAKE_NOTES.copy(),['C', 'B', 'A']),
    (FAKE_NOTES_EDGE_CASE.copy(),['A', 'B', 'C']),
    (FAKE_SINGLE_NOTE.copy(),['most_viewed']),
    ])
def test_pull_top_viewed(test_dict, expected):
   result = note_display.pull_top_viewed(test_dict)
   assert result == expected


@pytest.mark.parametrize("test_dict, expected",[
    (FAKE_MANY_NOTES.copy(),['most_viewed', 'second_most', 'third_most']),
    # Test notes are not sorted when num < 5:
    (FOUR_FAKE_NOTES.copy(),[]),
    (FAKE_SINGLE_NOTE.copy(),[])
    ])
def test_most_viewed(test_dict, expected):
    result = note_display.most_viewed(test_dict)
    assert result == expected


@pytest.mark.parametrize("test_dict, expected",[
    (FAKE_MANY_NOTES.copy(),'recently_opened'),
    ({}, None)
    ])
def test_find_last_opened(test_dict, expected):
    result = note_display.find_last_opened(test_dict)
    assert result == expected


@pytest.mark.parametrize("test_dict, expected",[
    (FAKE_MANY_NOTES.copy(),[
        'recently_opened',
        'most_viewed',
        'second_most',
        'third_most',
        'A',
        'fake_note_1',
        'Z',
        ]),
    # Test case where all views are the same.
    (FAKE_NOTES_EDGE_CASE.copy(), ['G', 'A', 'B', 'C', 'D', 'E', 'F']),
    (FOUR_FAKE_NOTES.copy(),['recently_opened', 'A', 'B', 'C']),
    (FAKE_SINGLE_NOTE.copy(),['most_viewed'])
    ])
def test_sort_notes(test_dict, expected):
    result = note_display.sort_notes(test_dict)
    assert result == expected


def test_listing_tags():
    def fake_return(input_param):
        return input_param
    
    with patch('foolscap.note_display.display_list') as mock_display,\
         patch('foolscap.note_display.load_meta') as mock_meta:
        mock_meta.return_value = FAKE_MANY_NOTES.copy()
        mock_display.side_effect = fake_return
        result = note_display.list_notes(None, 'tags')
        mock_display.assert_called_once()
        assert result == [{'title': 'fake_tag', 'description': str(7),
                           'sub_headings': [('A', 'This is a fake note'), 
                          ('fake_note_1', 'This is a fake note'), 
                          ('most_viewed', 'This is a fake note'), 
                          ('recently_opened', 'This is a fake note'), 
                          ('second_most', 'This is a fake note'), 
                          ('third_most', 'This is a fake note'), 
                          ('Z', 'This is a fake note')]}]


def test_count_tags():
    mock_notes = FAKE_MANY_NOTES.copy()
    result = note_display.count_tags(mock_notes)
    assert result.most_common(1)[0] == ('fake_tag', 7)


def test_get_by_tag():
    # Get all notes with tag: 'fake_tag'
    mock_notes = FAKE_MANY_NOTES.copy()
    result = note_display.get_by_tag(mock_notes, 'fake_tag')
    assert result == [('A', 'This is a fake note'), 
                      ('fake_note_1', 'This is a fake note'), 
                      ('most_viewed', 'This is a fake note'), 
                      ('recently_opened', 'This is a fake note'), 
                      ('second_most', 'This is a fake note'), 
                      ('third_most', 'This is a fake note'), 
                      ('Z', 'This is a fake note')]


def test_create_tag_display():
    # Get all notes with tag: 'fake_tag'
    mock_notes = FAKE_MANY_NOTES.copy()
    result = note_display.create_tag_display(mock_notes)
    assert result == [{'title': 'fake_tag', 'description': str(7),
                       'sub_headings': [('A', 'This is a fake note'), 
                      ('fake_note_1', 'This is a fake note'), 
                      ('most_viewed', 'This is a fake note'), 
                      ('recently_opened', 'This is a fake note'), 
                      ('second_most', 'This is a fake note'), 
                      ('third_most', 'This is a fake note'), 
                      ('Z', 'This is a fake note')]}]

