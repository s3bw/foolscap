import curses
from curses import panel

from .render_objects import Frame
from .render_objects import HelpBar
from .render_objects import StatusBar
from .render_objects import TitleBar
from .content_display import DisplayContents
from .key_listener import KeyListener


def display_list(display_data):
    """ Terminal Handler for curses programs.
        Setup curses context and tear down to terminal.

    :param display_data: (dict) data for display.
    :return: (string) indicating action to perform.
    """
    return curses.wrapper(setup_folio, display_data)


def setup_folio(stdscreen, display_data):
    # Called after curses __init__
    curses.curs_set(0)
    with FolioConsole(stdscreen, display_data) as folio_console:
        selected_action = folio_console.show()
    return selected_action


class FolioConsole:
    def __enter__(self):
        panel.update_panels()
        self.panel.hide()
        self.panel.top()
        self.panel.show()

        self.screen.keypad(1)
        self.screen.clear()
        return self

    def __exit__(self, _type, value, traceback):
        self.screen.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def __init__(self, stdscreen, items):
        self.items = items
        # self.expand_indexs = []
        self.screen = stdscreen.subwin(0, 0)
        self.panel = panel.new_panel(self.screen)
        self.count_notes = len(self.items)

        self.ui_collection()

        self.key_listener = KeyListener(self.screen, self.count_notes)

    def ui_collection(self):
        self.render_objects = []

        frame = Frame(self.screen)
        self.add_child(frame)

        status_bar = StatusBar(self.screen, self.count_notes)
        self.add_child(status_bar)

        title_bar = TitleBar(self.screen)
        self.add_child(title_bar)

        help_bar = HelpBar(self.screen)
        self.add_child(help_bar)

        self.list_content = DisplayContents(self.screen, self.items)
        self.add_child(self.list_content)

    def add_child(self, child_object):
        self.render_objects.append(child_object)

    def render_all(self):
        self.screen.clear()
        for child in self.render_objects:
            child.update()
            child.draw()

    def show(self):
        """ Displays Menus
        """
        selected_action = None
        while not selected_action:
            list_top, self.position = self.key_listener.get_position()
            self.list_content.update_pointers(list_top, self.position)

            self.render_all()
            selected_action, action_note = self.key_listener.get_action()
        return selected_action, self.items[action_note][0]

        # What happens if the expansion happens to the
        # expanded one above it?
        # elif key == curses.KEY_RIGHT:
        #     self.expand_indexs.append(cursor_position)

        # What happens if the you hit left mid way down
        # a expanded section?
        # elif key == curses.KEY_LEFT:
        #     self.expand_indexs.remove(cursor_position)

