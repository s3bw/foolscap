import curses


ENTER_KEY = [curses.KEY_ENTER, ord('\n')]
# BACKSPACE = curses.KEY_RESIZE
UP_ARROW = curses.KEY_UP
DOWN_ARROW = curses.KEY_DOWN


def _check_bounds(pos, max_len):
    if pos < 0:
        return max_len - 1
    if max_len <= pos:
        return 0
    return pos


def _move_up(position, max_len):
    position -= 1
    return _check_bounds(position, max_len)


def _move_down(position, max_len):
    position += 1
    return _check_bounds(position, max_len)


class HandleKeys():
    def __init__(self, screen, count_notes):
        self.screen = screen
        self.position = 0
        self.max_pos = count_notes
        self.command = None

    def get_action(self):
        command = self.command
        key = self.screen.getch()
        if key in ENTER_KEY:
            command = 'view'
        if key == ord('e'):
            command = 'edit'
        if key == ord('q'):
            exit()
        # elif key == BACKSPACE:
        #     self.screen.erase()
        elif key == UP_ARROW:
            self.position = _move_up(self.position, self.max_pos)
        elif key == DOWN_ARROW:
            self.position = _move_down(self.position, self.max_pos)

        self.command = command
        return self.command

    def get_position(self):
        return self.position


