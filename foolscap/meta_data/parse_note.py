import re


MAX_TITLE_LEN = 32


def replace_spaces(title):
    """ Replaces spaces contained in a title."""
    if ' ' in title:
        return title.replace(' ', '_')
    return title


def max_title_len(title):
    if len(title) > MAX_TITLE_LEN:
        print('\nTitle must be less than {} characters.'.format(MAX_TITLE_LEN))
        return title[:MAX_TITLE_LEN]
    return title


def lower_case(title):
    """ They should expect the title to be low case next time.
    """
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    contains_upper = any(char in title for char in alphabet_upper)
    if contains_upper:
        title = title.lower()
        print('\nTitle made lowercase: {}'.format(title))
    return title


def restrict_title(title):
    """
    This is implemented in two places:
        - new_components
        - update_component
    """
    title = max_title_len(title)
    title = replace_spaces(title)
    title = lower_case(title)
    return title


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

        return [
            (content[start], content[start + 1], start, end)
            if content[start]
            else ('Content line {}:'.format(start), content[start + 1])
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


def get_bookmacro(contents):
    bookline = contents[-3]
    book_pattern = re.compile("\{book:([a-z]*)\}")
    book = book_pattern.findall(bookline)
    if book:
        return book[0]
    else:
        return 'general'


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

