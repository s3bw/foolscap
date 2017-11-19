import curses
from curses import panel


def display_list(list_data):
    # print(list_data)
    curses.wrapper(setup_list_display, list_data)


def setup_list_display(stdscreen, list_data):
    screen = stdscreen
    curses.curs_set(0)

    main_menu = FoolScapMenu(list_data, screen)
    main_menu.display()


class FoolScapMenu(object):
    def __init__(self, items, stdscreen):
        self.screen = stdscreen.subwin(0, 0)
        self.screen.keypad(1)
        self.panel = panel.new_panel(self.screen)
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


    def help_line(self, bottom_line):
        help_string = " [q]uit "

        self.screen.addstr(bottom_line, 2, help_string)
        

    def draw_border(self):
        max_y, max_x = self.screen.getmaxyx()
        self.max_y, self.max_x = max_y, max_x

        self.screen.border('#', '#', '#', '#', '#', '#', '#', '#')
        self.screen.addstr(7, 2, "MaxY: {}".format(max_y))
        self.screen.addstr(8, 2, "MaxX: {}".format(max_x))

        self.help_line(max_y - 1)
        

    def render(self):
        self.screen.refresh()
        curses.doupdate()

        self.draw_border()
        self.centre_x = int(self.max_x/2)
        
        # Move to Function
        heading = "|   FoolScap   |"
        centre_heading = self.centre_x - int(len(heading)/2)
        self.screen.addstr(0, centre_heading, heading)

        cursor_position = self.position
        for index, item in enumerate(self.items):
            print_line = 1 + index
            mode = curses.A_NORMAL
            if index == cursor_position:
                mode = curses.A_REVERSE
            
            item_title, description = item
            option_title = " >  {}:".format(item_title)
            option_description = "{}".format(description)

            self.screen.addstr(print_line, 1, option_title, mode)
            if self.max_x > 50:
                self.screen.addstr(print_line, self.centre_x, option_description, mode)


    def handle_keys(self):
        cursor_position = self.position
        max_len = len(self.items) - 1
        enter_key = [curses.KEY_ENTER, ord('\n')]
        key = self.screen.getch()

        if key in enter_key:
            raise NotImplementedError 
            self.items[cursor_position][1]()

        if key == ord('q'):
            exit()

        #implement edit, from list

        elif key == curses.KEY_RESIZE:
            self.screen.erase()

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
        self.screen.clear()

        while True:
            self.render()
            self.handle_keys()

        # tscreenn
        self.screen.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
