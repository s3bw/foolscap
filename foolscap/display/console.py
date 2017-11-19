import curses
from curses import panel


def display_list(list_data):
    curses.wrapper(setup_list_display, list_data)


def setup_list_display(stdscreen, list_data):
    screen = stdscreen
    curses.curs_set(0)

    main_menu = FoolScapMenu(list_data, screen)
    main_menu.display()


class FoolScapMenu(object):
    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items


    def _check_bounds(self, new_pos, max_len):
        if new_pos < 0:
            return 0
        if max_len <= new_pos:
            return max_len
        return new_pos


    def move(self, n):
        # Key result
        self.position += n

        max_len = len(self.items) - 1
        return self._check_bounds(self.position, max_len)


    def render(self):
        self.window.refresh()
        curses.doupdate()

        cursor_position = self.position
        for index, item in enumerate(self.items):
            mode = curses.A_NORMAL
            if index == cursor_position:
                mode = curses.A_REVERSE

            menu_option = "--- {}".format(item)
            self.window.addstr(1 + index, 1, menu_option, mode)


    def handle_keys(self):
        cursor_position = self.position
        max_len = len(self.items) - 1
        enter_key = [curses.KEY_ENTER, ord('\n')]
        key = self.window.getch()

        if key in enter_key:
            raise NotImplementedError 
            self.items[cursor_position][1]()

        if key == ord('q'):
            exit()

        elif key == curses.KEY_UP:
            self.position = self.move(-1)

        elif key == curses.KEY_DOWN:
            self.position = self.move(1)


    def display(self):
        """ Displays Menus
        """
        # init render
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.render()
            self.handle_keys()

        # teardown
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
