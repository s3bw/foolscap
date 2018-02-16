import curses
from curses import panel

from foolscap.display.render_objects import Frame
from foolscap.display.render_objects import HelpBar
from foolscap.display.render_objects import StatusBar
from foolscap.display.render_objects import TitleBar
from foolscap.display.content_display import DisplayContents
from foolscap.display.key_listener import KeyListener


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
        expand_index = None
        while not selected_action:
            list_top, self.position = self.key_listener.get_position()

            self.menu_items = self.list_content.expand(expand_index)
            self.list_content.update_pointers(list_top, self.position)
            self.key_listener.set_max(len(self.menu_items))

            self.render_all()
            # Sort this mess out
            (selected_action,
             action_note,
             expand_index) = self.key_listener.get_action()
        return selected_action, self.menu_items[action_note].title

        # What happens if the expansion happens to the
        # expanded one above it?
        # elif key == curses.KEY_RIGHT:
        #     self.expand_indexs.append(cursor_position)

        # What happens if the you hit left mid way down
        # a expanded section?
        # elif key == curses.KEY_LEFT:
        #     self.expand_indexs.remove(cursor_position)

