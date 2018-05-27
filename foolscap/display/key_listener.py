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
        # add more key bindings here.

    def _update(self):
        self.scroll.update(self.max_pos)

        # Calculate max cursor position.
        if self.scroll.bottom_line - 2 > self.max_pos:
            self.max_cur_pos = self.max_pos
        else:
            self.max_cur_pos = self.scroll.bottom_line - 2

    def set_max(self, count_notes):
        self.max_pos = count_notes

    def get_action(self):
        self._update()
        toggle_expand = None
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
        # For a sense of power, left should collapse
        # and right should expand
        # elif key == LEFT_ARROW:
        #     self.drop_down.collapse()
        elif key == RIGHT_ARROW:
            toggle_expand = self.scroll.list_pointer
        # command handles foolscap functions
        # list pointer executes on note at pointer
        # toggle handle functions for display
        return self.command, self.scroll.list_pointer, toggle_expand

    def get_position(self):
        return self.scroll.list_top, self.scroll.position

