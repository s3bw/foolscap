

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


def get_title(note):
    # title parsing needs improvement (regex)
    return [line[2:] for line in note if line[:2] == '# ']

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


def get_moving_lines(note):
    _lines = [line for line in note if line[:1] == '>']
    return _lines

def parse_sub_headings(content):
    sub_headings_indexs = index_sub_headings(content)
    return [
        (content[index + 1], content[index + 2])
        if content[index + 1]
        else ('Content line {}:'.format(index + 1), content[index + 2])
        for index in sub_headings_indexs
    ]


def index_sub_headings(content):
    return [index
            for index, line in enumerate(content[2:])
            if line and line[0] == ':']



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



