import curses


ENTER_KEY = [curses.KEY_ENTER, ord('\n')]
# BACKSPACE = curses.KEY_RESIZE
UP_ARROW = curses.KEY_UP
DOWN_ARROW = curses.KEY_DOWN


class HandleKeys():
    def __init__(self, screen, count_notes):
        self.screen = screen
        self.position = 1
        self.list_pointer = 0
        self.list_top = 0
        self.max_pos = count_notes
        self.command = None
        self.update()

    def update(self):
        self.top_line = 0
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_line = self.max_y - 1
        self.centre_x = int(self.max_x / 2)

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

    def get_action(self):
        self.update()
        key = self.screen.getch()
        if key in ENTER_KEY:
            self.command = 'view'
        if key == ord('e'):
            self.command = 'edit'
        if key == ord('q'):
            exit()
        # elif key == BACKSPACE:
        #     self.screen.erase()
        elif key == UP_ARROW:
            self.move_up()
        elif key == DOWN_ARROW:
            self.move_down()
        return self.command, self.list_pointer

    def get_position(self):
        return self.list_top, self.position


