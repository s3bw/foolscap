from .root_screen import Terminal


class Scrollable(Terminal):
    def __init__(self, screen, max_pos):
        Terminal.__init__(self, screen)
        self.position = 1
        self.list_top = 0
        self.list_pointer = 0
        self.max_pos = max_pos

    def update(self, max_pos):
        Terminal.update(self)
        self.max_pos = max_pos

    def move_up(self):
        """
        :param list_pointer: (int) note being actioned upon
        :param position: (int) cursor position
        :param list_top: (int) index of note at 1st line
        :param max_pos: (int) maximum number of positions
        """
        # list pointer at 0 and up is pressed
        if self.list_pointer <= 0:
            self.list_pointer = self.max_pos - 1
            # position for small/large terminal max_y
            if self.max_pos < self.bottom_line - 1:
                self.position = self.max_pos
            else:
                self.position = self.bottom_line - 2
            # top note pointer for small/large terminal max_y
            if self.max_pos < self.bottom_line - 1:
                self.list_top = 0
            else:
                dy = (self.bottom_line - 1 - self.top_line - 1)
                self.list_top = self.max_pos - dy
        # position at top line and when list_pointer hasn't reached 0
        elif self.position == self.top_line + 1:
            self.list_pointer -= 1
            if self.max_pos > self.bottom_line - 1:
                self.list_top -= 1
        # position not at top
        else:
            self.position -= 1
            self.list_pointer -= 1

    def move_down(self):
        # reached last note
        if self.list_pointer == self.max_pos - 1:
            self.list_pointer = 0
            self.position = 1
            self.list_top = 0
        # reached bottom line
        elif self.position == self.bottom_line - 2:
            self.list_pointer += 1
            self.list_top += 1
        # in the middle
        else:
            self.position += 1
            self.list_pointer += 1

