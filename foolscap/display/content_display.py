import curses

from foolscap.display.root_screen import Terminal


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE

TITLE = "|>  {}"
DESCRIPTION = "  {}"
EXPANDABLE = "+ {}"


def _set_colour(line, cursor):
    if line == cursor:
        return REVERSE_LINE_COLOUR
    if line % 2 == 0:
        return DIM_LINE_COLOUR
    return NORMAL_LINE_COLOUR


class DisplayContents(Terminal):
    def __init__(self, screen, items):
        Terminal.__init__(self, screen)
        self.items = items

    def update_pointers(self, first_index, cursor):
        self.first_index = first_index
        self.cursor = cursor

    def get_item(self, index):
        z = None
        x = self.items[index]['title']
        y = self.items[index]['description']
        if 'sub_headings' in self.items[index]:
            z = self.items[index]['sub_headings']
            y = EXPANDABLE.format(y)
        else:
            y = DESCRIPTION.format(y)

        return TITLE.format(x), y, z

    def draw(self):
        """
        'top_note' first note in list
        """
        index = self.first_index
        for line_y in range(self.top_line + 1, self.bottom_line - 1):
            if index > len(self.items) - 1:
                break

            line_colour = _set_colour(line_y, self.cursor)
            title, desc, sub_headings = self.get_item(index)

            self.screen.addstr(line_y, 0, title, line_colour)
            if self.max_x > 64:
                self.screen.addstr(line_y, self.centre_x - 2,
                                   desc, line_colour)
            index += 1


