import re
from string import ascii_uppercase


MAX_TITLE_LEN = 32
INVALID_CHARS = "\nTitle can not contain these characters: '{}'"
INVALID_LENGTH = "\nTitle must be less than {} characters."
INVALID_CASE = "\nTitle made lowercase: {}"


def replace_illegal_characters(title):
    """ Replaces illegal characters contained in a title."""
    illegal_characters = ' @:'
    if any(char in title for char in illegal_characters):
        print(INVALID_CHARS.format(illegal_characters))
        for char in illegal_characters:
            title = title.replace(char, '_')
    return title


def max_title_len(title):
    if len(title) > MAX_TITLE_LEN:
        print(INVALID_LENGTH.format(MAX_TITLE_LEN))
        return title[:MAX_TITLE_LEN]
    return title


def lower_case(title):
    """ They should expect the title to be low case next time.
    """
    contains_upper = any(char in title for char in ascii_uppercase)
    if contains_upper:
        title = title.lower()
        print(INVALID_CASE.format(title))
    return title


def restrict_title(title):
    """
    This is implemented in two places:
        - new_components
        - update_component
    """
    title = max_title_len(title)
    title = replace_illegal_characters(title)
    title = lower_case(title)
    return title


def name(name):
    """Breakdown components of title.

    Notes can contain '@' followed by start and end indices.
        This determines the snippet of note to display.
    """
    _min, _max = 0, 0
    if '@' in name:
        try:
            note_name, minmax = name.split('@')
            _min, _max = minmax.split(':')
            _min = int(_min) + 2
            _max = int(_max) + 1
        except ValueError:
            raise ValueError("Name '{}' not valid!".format(name))
        return note_name, _min, _max
    return name, _min, _max


def get_title(note):
    # title parsing needs improvement (regex)
    return [line[2:] for line in note if line[:2] == '# ']


def get_moving_lines(note):
    _lines = [line for line in note if line[:1] == '>']
    return _lines


def double_items(iterable):
    """ Given [1, 2, 3]

    Returns [1, 1, 2, 2, 3, 3]
    """
    return [item for tup in zip(iterable, iterable) for item in tup]


def index_pairs(indexes, content):
    """ We extract the generator contents and remove
        the first pair.

    The first pair won't have a title as it's
       between the start and first section the
       content here should likely be an introduction
       for the entire note.
    """
    start = [1]
    end = [len(content) - 1]

    indexes = start + double_items(indexes) + end
    paired = pairwise(indexes)
    return [n for n in paired][1:]


def index_sub_headings(content):
    """ A note with the following, will return [10]

        10.. Section 1:
        11.. :A new section
    """
    return [index + 1
            for index, line in enumerate(content[2:])
            if line and line[0] == ':']


def parse_sub_headings(content):
    """ Index such as [10]
    will return [("section title", "section description", 10, int:[end])]

    From note:
        10.. Section 1:
        11.. :A new section
    """
    heading_indexs = index_sub_headings(content)
    if heading_indexs:
        index_pair = index_pairs(heading_indexs, content)
        content_title = "Content line {}:"

        return [
            (content[start], content[start + 1], start, end)
            if content[start]
            else (content_title.format(start), content[start + 1], start, end)
            for start, end in index_pair
        ]


def get_contents(note):
    """ Get note content.

    Looks for '==' lines and extract only that which
        is between them.

    parse_text.pairwise in this case, pairs sets of content-indexes
    """
    content_index = [
        index
        for index, line
        in enumerate(note)
        if line[:2] == '=='
    ]
    # This should only deal with one Note, split notes then get content.
    indexes = pairwise(content_index)

    # for start, end in indexes:
    content = [note[start:end + 1] for start, end in indexes]

    return content


def note_description(content):
    # Needs to return multiple descriptions (sectioning)
    description = content[1]
    if description and description[0] == ':':
        return description[1:].lstrip()


def note_tags(contents):
    tag_line = contents[-2]

    if tag_line and '{' in tag_line:
        tags = [tag[1:-1] for tag in tag_line.split(' ') if tag]
        return tags


def get_macro(macro, contents):
    macroline = contents[-3]
    macro_pattern = re.compile("\{" + macro + ":([a-zA-Z0-9]*)\}")
    setting = macro_pattern.findall(macroline)
    if setting:
        return setting[0]
    else:
        return None


def pairwise(iterable):
    """ Pairs even length iterables.

    Returns:
        (:obj:list[tuple]) paired tuples

    Example:
        >>> pairwise([1, 2, 3, 4])
        [(1, 2), (3, 4)]
    """
    # Do I throw error for odd length iterable?
    a = iter(iterable)
    return zip(a, a)

