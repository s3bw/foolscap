"""Note class.

Open Questions:
- How would I turn this from JSON<->Object
- How would I find the conflict in names


"""


class Note:

    def __init__(self, title, content):
        title = restrict_title(title)
        self.title = unique_text(title)

        save_text(title, content)

        self.views = 0
        self.created = datetime.now()
        self.update(title, content)

    def update(self, title, content):
        self.views += 1
        self.length = len(content)
        self.modified = datetime.now()
        self.description = note_description(content)

        # Diff tags
        self.tags = note_tags(content)

        # Return 'general' in get_macro?
        book = get_macro('book', content)
        self.book = book if book else 'general'

        self.vim_cmds = []
        textwidth = get_macro('textwidth', content)
        set_width = ":set textwidth={}".format(textwidth)
        if textwidth:
            self.vim_cmds.append(set_width)

        self.sub_headings = parse_sub_headings(content)
        self.num_sub = len(self.sub_headings)


