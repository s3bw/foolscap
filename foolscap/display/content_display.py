import curses

from .root_widget import Displayable


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE

TITLE = "|>  {}"
DESCRIPTION = "{}"


def _set_colour(line, cursor):
    if line == cursor:
        return REVERSE_LINE_COLOUR
    if line % 2 == 0:
        return DIM_LINE_COLOUR
    return NORMAL_LINE_COLOUR


class DisplayContents(Displayable):
    def __init__(self, screen, items):
        Displayable.__init__(self, screen)
        self.items = items

    def update_position(self, position):
        self.position = position

    def draw(self):
        for index, item in enumerate(self.items):
            line_colour = _set_colour(index, self.position)

            item_title, description = item
            item_title = TITLE.format(item_title)
            item_description = DESCRIPTION.format(description)

            self.screen.addstr(index + 1, 0, item_title, line_colour)
            if self.max_x > 64:
                self.screen.addstr(index + 1, self.centre_x,
                                   item_description, line_colour)


