import curses
from curses import panel


def display_list(list_data):
    # print(list_data)
    return curses.wrapper(setup_list_display, list_data)


def setup_list_display(stdscreen, list_data):
    screen = stdscreen
    curses.curs_set(0)

    main_menu = FoolScapMenu(list_data, screen)
    return main_menu.run_display()


class FoolScapMenu(object):
    def __init__(self, items, stdscreen):
        self.screen = stdscreen.subwin(0, 0)
        self.screen.keypad(1)
        self.panel = panel.new_panel(self.screen)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items

    def render(self):
        def _draw_border(y, x):
            bottom_line = y - 1

            self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
            self.screen.addstr(y - 6, 2, "MaxY: {}".format(y))
            self.screen.addstr(y - 5, 2, "MaxX: {}".format(x))

            help_string = " [q]uit ### [e]dit ### [d]elete "
            self.screen.addstr(bottom_line, 2, help_string)

        self.screen.refresh()
        curses.doupdate()

        self.max_y, self.max_x = self.screen.getmaxyx()
        self.centre_x = int(self.max_x / 2)

        _draw_border(self.max_y, self.max_x)

        # Move to Function
        heading = "|   FoolScap   |"
        centre_heading = self.centre_x - int(len(heading) / 2)
        self.screen.addstr(0, centre_heading, heading)

        cursor_position = self.position
        for index, item in enumerate(self.items):
            print_line = 1 + index

            mode = curses.A_NORMAL
            if index % 2 == 0:
                mode = curses.A_DIM
            if index == cursor_position:
                mode = curses.A_REVERSE

            item_title, description = item
            option_title = " >  {}:".format(item_title)
            option_description = "{}".format(description)

            self.screen.addstr(print_line, 1, option_title, mode)
            if self.max_x > 50:
                self.screen.addstr(
                    print_line,
                    self.centre_x,
                    option_description,
                    mode
                )

    def handle_keys(self):

        def _check_bounds(new_pos, max_len):
            if new_pos < 0:
                return 0
            if max_len <= new_pos:
                return max_len
            return new_pos

        def _move(position, n):
            # Key result
            position += n

            max_len = len(self.items) - 1
            return _check_bounds(position, max_len)

        cursor_position = self.position

        key = self.screen.getch()
        enter_key = [curses.KEY_ENTER, ord('\n')]

        if key in enter_key:
            return ('view', self.items[cursor_position][0])

        if key == ord('e'):
            return ('edit', self.items[cursor_position][0])

        if key == ord('q'):
            exit()

        elif key == curses.KEY_RESIZE:
            self.screen.erase()

        elif key == curses.KEY_UP:
            self.position = _move(cursor_position, -1)

        elif key == curses.KEY_DOWN:
            self.position = _move(cursor_position, 1)

    def run_display(self):
        """ Displays Menus
        """
        # init render
        self.panel.top()
        self.panel.show()
        self.screen.clear()

        new_action = None
        while not new_action:
            self.render()
            new_action = self.handle_keys()

        # tscreenn
        self.screen.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
        return new_action
