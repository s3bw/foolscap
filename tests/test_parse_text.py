import pkg_resources

import parse_text


TEST_NOTE = pkg_resources.resource_filename(
    __name__,
    'data/test_note.txt'
)

EXPECTED_NOTE = """
# note_is_test
====================
:Description of note

Some content.
>Move content.

{test} {unit}
====================

"""


# I should do multiple notes with different results,
# No lines to move, lines to move.
# What happens with no title?
# also "section" needs to be renamed to "title"
# setUp() and tearDown() methods.


def test_loading_in_note():
    note = parse_text.load_text(TEST_NOTE)

    assert note == EXPECTED_NOTE.split('\n')
    assert len(note) == 12


def test_getting_of_sections():
    note = EXPECTED_NOTE.split('\n')

    section = parse_text.get_sections(note)
    assert section == ['note_is_test']
    assert len(section) == 1


def test_get_contents():
    note = EXPECTED_NOTE.split('\n')
    content = parse_text.get_contents(note)
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


def test_getting_of_note_description():
    note = EXPECTED_NOTE.split('\n')
    content = parse_text.get_contents(note)[0]
    description = parse_text.note_description(content)
    assert description == ':Description of note'


def test_note_tags():
    note = EXPECTED_NOTE.split('\n')
    content = parse_text.get_contents(note)[0]
    tags = parse_text.note_tags(content)
    expected_tags = ['test', 'unit']
    assert tags == expected_tags


# def test_getting_of_moving_lines():
    # note = EXPECTED_NOTE.split('\n')
