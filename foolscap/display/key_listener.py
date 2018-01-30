import curses

from .key_objects import Scrollable


ENTER_KEY = [curses.KEY_ENTER, ord('\n')]
# BACKSPACE = curses.KEY_RESIZE
UP_ARROW = curses.KEY_UP
DOWN_ARROW = curses.KEY_DOWN


class KeyListener:
    def __init__(self, screen, count_notes):
        self.screen = screen
        self.max_pos = count_notes
        self.command = None

        self.scroll = Scrollable(self.screen, self.max_pos)
        # add more key bindings here.

    def _update(self):
        self.scroll.update(self.max_pos)

    def get_action(self):
        self._update()
        key = self.screen.getch()
        if key in ENTER_KEY:
            self.command = 'view'
        if key == ord('e'):
            self.command = 'edit'
        if key == ord('q'):
            exit()
        elif key == UP_ARROW:
            self.scroll.move_up()
        elif key == DOWN_ARROW:
            self.scroll.move_down()
        return self.command, self.scroll.list_pointer

    def get_position(self):
        return self.scroll.list_top, self.scroll.position


