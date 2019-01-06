import os
from abc import ABC
from abc import abstractmethod
from curses import A_REVERSE as REVERSE
from curses import A_NORMAL as NORMAL


# Left Separator Normal
LSN = ('', NORMAL)
# Left Separator Reverse
LSR = ('', REVERSE)
# Alternative Left Separator Normal
ALSN = ('', NORMAL)
# Alternative Left Separator Reverse
ALSR = ('', REVERSE)

HELP_OPTIONS = [
    '| 0/5    [H]elp   |',
    '| 1/5   e[X]port  |',
    '| 2/5  [->]expand |',
    '| 3/5   [d]elete  |',
    '| 4/5    [e]dit   |',
    '| 5/5    [q]uit   |',
]
ROOT = ['~']


class Widget(ABC):
    """A base terminal widget."""

    top_line = 0

    def update_screen(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_line = self.max_y - 1
        self.centre_x = int(self.max_x / 2)

    def attach_screen(self, screen):
        self.screen = screen
        self.update_screen()

    def update(self):
        self.update_screen()

    @abstractmethod
    def draw(self):
        raise NotImplementedError


class TabBar(Widget):
    """Draws the books as tabs in the display."""

    def __init__(self, screen, book, books):
        self.attach_screen(screen)
        self.tabs = [book]
        if book in books:
            self.tabs = ['general']
            books = set(books)
            books.remove('general')
            self.tabs.extend(sorted(books))
            self.highlight_index = self.tabs.index(book)
        else:
            self.highlight_index = 0

        self.start_x = 5

    def next_tab(self):
        """Go to next tab."""
        self.highlight_index += 1
        if self.highlight_index == len(self.tabs):
            self.highlight_index = 0
        return self.tabs[self.highlight_index]

    def prev_tab(self):
        """Go to previous tab."""
        self.highlight_index -= 1
        if self.highlight_index < 0:
            self.highlight_index = len(self.tabs) - 1
        return self.tabs[self.highlight_index]

    def _draw_sep(self, x, sep):
        character, colour = sep
        self.screen.addstr(self.top_line, x, character, colour)

    def draw_first_sep(self):
        if self.highlight_index == 0:
            self._draw_sep(self.start_x, LSR)
        else:
            self._draw_sep(self.start_x, ALSN)

    def draw_last_sep(self, x_pos):
        if len(self.tabs) == self.highlight_index + 1:
            self._draw_sep(x_pos, LSN)
        else:
            self._draw_sep(x_pos, ALSN)

    def draw_sep(self, index, x_pos):
        if index == 0:
            self.draw_first_sep()
        elif index - 1 == self.highlight_index:
            self._draw_sep(x_pos, LSN)
        elif index == self.highlight_index:
            self._draw_sep(x_pos, LSR)
        else:
            self._draw_sep(x_pos, ALSN)

    def draw(self):
        draw_x = self.start_x
        for index, tab_name in enumerate(self.tabs):
            self.draw_sep(index, draw_x)
            write = ' {} '.format(tab_name)
            line_colour = NORMAL
            if index == self.highlight_index:
                line_colour = REVERSE
            self.screen.addstr(self.top_line, draw_x + 1, write, line_colour)
            draw_x += len(write) + 1
        self.draw_last_sep(draw_x)


class Frame(Widget):

    def __init__(self, screen):
        self.attach_screen(screen)

    def draw(self):
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')


class StatusBar(Widget):
    """Aggregating should happen in this widget."""
    display_text = ''

    def __init__(self, screen, items, model):
        self.attach_screen(screen)
        note_count = len(items)
        self.display_text += "Notes: {}".format(note_count)

        tag_count = sum([
            len(model.get_value(item, 'tags'))
            for item in items
        ])
        ave_tags = tag_count / note_count
        self.display_text += " | Ave tags: {0:.2f}".format(ave_tags)

    def draw(self):
        self.screen.addstr(self.bottom_line - 1, 2, self.display_text)


class HelpBar(Widget):
    """Constructs the help bar"""

    def __init__(self, screen):
        self.attach_screen(screen)
        self.help_options = HELP_OPTIONS
        self.shown = 0
        self.build_help()

    def next_hint(self):
        self.shown += 1
        if self.shown == len(self.help_options):
            self.shown = 0

    def build_help(self):
        adjust_x = self.max_x - 6
        if adjust_x < len(self.help_options[0]):
            self.help_string = ''
        else:
            self.help_string = self.help_options[self.shown]

    def draw(self):
        self.screen.addstr(self.bottom_line, 2, self.help_string)

    def update(self):
        self.build_help()
        self.update_screen()


class TitleBar(Widget):
    """Construct the title and path"""

    heading = "|   FoolScap   |"

    def __init__(self, screen):
        self.attach_screen(screen)
        self.centre_header = int((self.max_x - len(self.heading)) / 2)
        path = os.path.normpath(os.getcwd())
        self.cwd = self.format_path(path)

    def format_path(self, path):
        def _path_len(x):
            return self.centre_header + len(x) + 25

        path = path.split(os.sep)
        current_dir = [path[-1]]
        path = path[:-1]

        if 'home' in path[1]:
            path = path[3:]

        index = 0
        potential_path = os.sep.join(ROOT + path + current_dir)
        path_edge = _path_len(potential_path)
        path_parts = len(path)

        while path_edge > self.max_x:
            if index < path_parts:
                path[index] = '-'
                potential_path = os.sep.join(ROOT + path + current_dir)
                path_edge = _path_len(potential_path)
                index += 1
            elif index == path_parts:
                potential_path = current_dir[0]
                path_edge = _path_len(potential_path)
                index += 1
            elif index > path_parts:
                return ''

        return '| ' + potential_path + ' |'

    def draw(self):
        if self.max_x > 15:
            self.screen.addstr(self.top_line, self.centre_header, self.heading)
        if self.max_x > 25:
            self.screen.addstr(self.top_line, self.centre_header + 20, self.cwd)

    def update(self):
        self.update_screen()
        self.centre_header = int((self.max_x - len(self.heading)) / 2)
        path = os.path.normpath(os.getcwd())
        self.cwd = self.format_path(path)
