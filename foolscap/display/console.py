import curses
from curses import panel

from foolscap.display.menu import DisplayMenu
from foolscap.display.key_listener import KeyListener
from foolscap.display.render_composite import Frame
from foolscap.display.render_composite import HelpBar
from foolscap.display.render_composite import StatusBar
from foolscap.display.render_composite import TitleBar


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
        self.count_notes = len(items)
        self.screen = stdscreen.subwin(0, 0)
        self.panel = panel.new_panel(self.screen)

        self.ui_collection()

        self.key_listener = KeyListener(self.screen, self.count_notes)

    def ui_collection(self):
        frame = Frame(self.screen)
        status_bar = StatusBar(self.screen, self.count_notes)
        title_bar = TitleBar(self.screen)
        self.help_bar = HelpBar(self.screen)
        self.menu = DisplayMenu(self.screen, self.items)

        self.render_objects = [
            frame,
            status_bar,
            title_bar,
            self.help_bar,
            self.menu
        ]

    def render_all(self):
        self.screen.clear()
        for child in self.render_objects:
            child.update()
            child.draw()

    def show(self):
        """Displays Menus
        """
        selected_action = None
        selected_index = None
        while not selected_action:
            list_top, self.position = self.key_listener.get_position()

            self.menu.update_pointers(list_top, self.position)
            self.key_listener.set_max(len(self.menu))

            self.render_all()
            (selected_action,
             selected_index) = self.key_listener.get_action()

            if selected_action == 'help':
                self.help_bar.next_hint()
                selected_action = None
            if selected_action == 'expand':
                self.menu.expand_item(selected_index)
                selected_action = None

        return selected_action, self.menu.select_item(selected_index)
