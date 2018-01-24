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

    def update_pointers(self, top_note, position):
        self.top_note = top_note
        self.position = position

    def draw(self):
        """
        'top_note' first note in list

        """
        print_note = self.top_note
        for line_y in range(self.top_line + 1, self.bottom_line - 2):
            if print_note > len(self.items) - 1:
                break

            line_colour = _set_colour(line_y, self.position)
            note_title, note_desc = self.items[print_note]
            note_title = TITLE.format(note_title)
            note_desc = DESCRIPTION.format(note_desc)
            self.screen.addstr(line_y, 0, note_title, line_colour)
            if self.max_x > 64:
                self.screen.addstr(line_y, self.centre_x,
                                   note_desc, line_colour)
            print_note += 1


