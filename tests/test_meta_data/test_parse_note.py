import contextlib
from io import StringIO

import pytest

# from foolscap.handle_note_io import load_text
import foolscap.meta_data.parse_note as parse_note


def test_replace_spaces():
    result = parse_note.replace_spaces('note title')
    assert result == 'note_title'


def test_max_title_len():
    test_title = 'note_title_which_is_a_little_too_long'
    TITLE_LEN = parse_note.MAX_TITLE_LEN
    output = "Title must be less than {} characters."
    expected = output.format(TITLE_LEN)

    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        result = parse_note.max_title_len(test_title)
    output = temp_stdout.getvalue().strip()
    assert output == expected
    assert result == test_title[:TITLE_LEN]


def test_lower_case():
    result = parse_note.lower_case('NOTE_TITLE')
    assert result == 'note_title'


def test_restict_title():
    result = parse_note.restrict_title('note TITle')
    assert result == 'note_title'


EXPECTED_NOTE = """
# test_note
====================
:Description of note

Some content.
>Move content.

{test} {unit}
===================="""
def test_get_titles():
    note = EXPECTED_NOTE.split('\n')
    section = parse_note.get_title(note)
    assert section == ['test_note']
    assert len(section) == 1


def test_get_moving_lines():
    note = EXPECTED_NOTE.split('\n')
    moving_lines = parse_note.get_moving_lines(note)
    assert moving_lines == ['>Move content.']


@pytest.mark.parametrize("mock_content, expected",
    [([ '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],
        [('Sub Title:', ':testing subtitles', 3, 6)]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],
        [('Sub Title:', ':testing subtitles', 3, 6),
         ('Sub Title:', ':testing subtitles', 6, 9)]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        'testing subtitles',
        '',
        '===================='],
        None)])
def test_parse_sub_headings(mock_content, expected):
    result = parse_note.parse_sub_headings(mock_content)
    assert result == expected


@pytest.mark.parametrize("mock_content, expected",
    [([ '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],[3]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        'Sub Title:',
        ':testing subtitles',
        '',
        '===================='],[3,6]),
    ([  '====================', 
        ':Description of note', 
        '',
        'Sub Title:',
        'testing subtitles',
        '',
        '===================='],[])])
def test_index_sub_headings(mock_content, expected):
    result = parse_note.index_sub_headings(mock_content)
    assert result == expected


def test_get_contents():
    note = EXPECTED_NOTE.split('\n')
    content = parse_note.get_contents(note)
    expected_content = [[
        '====================', 
        ':Description of note', 
        '', 
        'Some content.', 
        '>Move content.', 
        '', 
        '{test} {unit}', 
        '===================='
    ]]
    assert content == expected_content


def test_note_description():
    fake_content = ['', ':Description of note', '']
    description = parse_note.note_description(fake_content)
    assert description == 'Description of note'

    fake_content = ['', ':    My awesome note', '']
    result = parse_note.note_description(fake_content)
    assert result == 'My awesome note'


def test_note_tags():
    note = EXPECTED_NOTE.split('\n')
    content = parse_note.get_contents(note)[0]
    tags = parse_note.note_tags(content)
    expected_tags = ['test', 'unit']
    assert tags == expected_tags


def test_pairwise():
    input_arg = [1, 2, 3, 4]
    result = list(parse_note.pairwise(input_arg))
    assert result == [(1, 2), (3, 4)]
