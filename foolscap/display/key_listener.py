import curses

from foolscap.display.key_objects import Scrollable


ENTER_KEY = [curses.KEY_ENTER, ord('\n')]
UP_ARROW = curses.KEY_UP
DOWN_ARROW = curses.KEY_DOWN
RIGHT_ARROW = curses.KEY_RIGHT
LEFT_ARROW = curses.KEY_LEFT


class KeyListener:
    def __init__(self, screen, count_notes):
        self.screen = screen
        self.max_pos = count_notes
        self.command = None

        self.scroll = Scrollable(self.screen, self.max_pos)

    def _update(self):
        """Update Scrollable objects' max position and the max
            position for the cursor on the list.
        """
        self.scroll.update(self.max_pos)

        # Calculate max cursor position.
        if self.scroll.bottom_line - 2 > self.max_pos:
            self.max_cur_pos = self.max_pos
        else:
            self.max_cur_pos = self.scroll.bottom_line - 2

    def set_max(self, count_notes):
        """Set the max position by the number of notes.

        :param int count_notes: number of notes in the list.
        """
        self.max_pos = count_notes

    def get_action(self):
        """Return action dictated by the pressed key.
        """
        self._update()
        self.command = None
        key = self.screen.getch()
        if key in ENTER_KEY:
            self.command = 'view'
        if key == ord('e'):
            self.command = 'edit'
        if key == ord('X'):
            self.command = 'export'
        if key == ord('q'):
            exit()
            # self.command = 'quit'
        elif key == UP_ARROW:
            self.scroll.move_up()
        elif key == DOWN_ARROW:
            self.scroll.move_down()
        elif key == ord('g'):
            # Move to top note
            self.scroll.move_to_position(1)
        elif key == ord('G'):
            # Move to bottom note
            self.scroll.move_to_position(self.max_cur_pos)
        elif key == ord('H'):
            # rotate the help bar
            self.command = 'help'
        elif key == RIGHT_ARROW:
            self.command = 'expand'
        return self.command, self.scroll.list_pointer

    def get_position(self):
        """Return the note at the top of the list and the cursor
            position.
        """
        return self.scroll.list_top, self.scroll.position

