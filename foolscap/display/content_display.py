import curses

from .root_widget import Displayable


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE

TITLE = "|>  {}"
DESCRIPTION = "{}"
INDICATE_SCROLL = "\t\t V~V~V MORE V~V~V "


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

    def update_pointers(self, first_index, cursor):
        self.first_index = first_index
        self.cursor = cursor

    def get_item(self, index):
        x, y = self.items[index]
        return TITLE.format(x), DESCRIPTION.format(y)

    def draw(self):
        """
        'top_note' first note in list

        """
        index = self.first_index
        for line_y in range(self.top_line + 1, self.bottom_line - 1):
            if index > len(self.items) - 1:
                break

            line_colour = _set_colour(line_y, self.cursor)
            title, desc = self.get_item(index)

            self.screen.addstr(line_y, 0, title, line_colour)
            if self.max_x > 64:
                self.screen.addstr(line_y, self.centre_x,
                                   desc, line_colour)
            index += 1


