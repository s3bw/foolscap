import os
from abc import ABC
from abc import abstractmethod


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


class Frame(Widget):

    def __init__(self, screen):
        self.attach_screen(screen)

    def draw(self):
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')


class StatusBar(Widget):
    def __init__(self, screen, n_notes):
        self.attach_screen(screen)
        display_text = "Notes: {}".format(n_notes)
        self.display_text = display_text

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
