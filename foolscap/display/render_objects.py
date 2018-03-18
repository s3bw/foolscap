import os

from foolscap.display.root_screen import Terminal


HELP_OPTIONS = [
    ' [q]uit ',
    ' [e]dit ',
    ' [d]elete ',
    ' [->]expand ',
    ' e[X]port ',
]


class Frame(Terminal):
    def __init__(self, screen, frame_type='default'):
        Terminal.__init__(self, screen)

    def draw(self):
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def update(self):
        Terminal.update(self)


class HelpBar(Terminal):
    def __init__(self, screen):
        Terminal.__init__(self, screen)
        self.build_help()

    def build_help(self):
        shown = 0
        adjust_x = self.max_x - 6

        potential_string = '--'.join(HELP_OPTIONS[:shown + 1])
        while len(potential_string) < adjust_x:
            shown += 1
            potential_string = '--'.join(HELP_OPTIONS[:shown + 1])
            if len(HELP_OPTIONS) <= shown:
                break

        self.help_string = '--'.join(HELP_OPTIONS[:shown])

    def draw(self):
        self.screen.addstr(self.bottom_line, 2, self.help_string)

    def update(self):
        self.build_help()
        Terminal.update(self)


class TitleBar(Terminal):
    def __init__(self, screen):
        Terminal.__init__(self, screen)
        self.heading = "|   FoolScap   |"
        path = os.path.normpath(os.getcwd())
        self.cwd = self.format_path(path)

    def format_path(self, path):
        path = path.split(os.sep)
        if 'home' in path[1]:
            path = os.sep.join(['~'] + path[3:])
            return '| ' + path + ' |'

    def draw(self):
        self.screen.addstr(self.top_line, self.centre_header, self.heading)
        self.screen.addstr(self.top_line, self.centre_header + 20, self.cwd)

    def update(self):
        Terminal.update(self)
        self.centre_header = int((self.max_x - len(self.heading)) / 2)


class StatusBar(Terminal):
    def __init__(self, screen, n_notes):
        Terminal.__init__(self, screen)
        display_text = "Notes: {}".format(n_notes)
        self.display_text = display_text

    def draw(self):
        self.screen.addstr(self.bottom_line - 1, 2, self.display_text)

    def update(self):
        Terminal.update(self)

