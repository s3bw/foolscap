import curses
from curses import panel

from foolscap.display.menu import DisplayMenu
from foolscap.display.key_listener import KeyListener
from foolscap.display.render_composite import Frame
from foolscap.display.render_composite import HelpBar
from foolscap.display.render_composite import StatusBar
from foolscap.display.render_composite import TitleBar
from foolscap.display.render_composite import TabBar


def display_list_v2(display_data):
    """Transform foolscap to fool."""
    from fool import console
    # from foolscap.displays import tag_view
    from foolscap.displays import view_notes

    model = display_data['model']
    data = {
        'items': [model.get(item) for item in display_data['titles']],
        'books': display_data['books'],
        'book': display_data['tab_title'],
    }
    for item, noteTitle in zip(data['items'], display_data['titles']):
        # print(item)
        item['more'] = 'anything'
        item['title'] = noteTitle
        if 'sub_headings' not in item.keys():
            item['sub_headings'] = {}
        else:
            subHeading = []
            for h in item['sub_headings']:
                title = h[0]
                description = h[1]
                subHeading.append({
                    'title': title,
                    'description': description,
                })
            item['sub_headings'] = subHeading
    # if model type tags, use tags view.
    # if model type notes use notes view.

    return console.display(view_notes, data, close='q')


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

    def __init__(self, stdscreen, data):
        self.items = data['titles']
        self.model = data['model']
        self.books = data['books']
        self.tab_title = data['tab_title']
        self.screen = stdscreen.subwin(0, 0)
        self.panel = panel.new_panel(self.screen)

        self.ui_collection()

        self.key_listener = KeyListener(self.screen, len(self.items))

    def ui_collection(self):
        frame = Frame(self.screen)
        status_bar = StatusBar(self.screen, self.items, self.model)
        title_bar = TitleBar(self.screen)
        self.help_bar = HelpBar(self.screen)
        self.tabs = TabBar(self.screen, self.tab_title, self.books)
        if self.model.model_type == 'tags':
            self.tabs = TabBar(self.screen, self.model.model_type, self.books)
        self.menu = DisplayMenu(self.screen, self.items, self.model)

        self.render_objects = [
            frame, status_bar, title_bar, self.help_bar, self.tabs, self.menu
        ]

    def render_all(self):
        self.screen.clear()
        for child in self.render_objects:
            child.update()
            child.draw()

    def show(self):
        """Displays Menus
        """
        selected = {'action': None, 'index': None}
        while not selected['action']:
            list_top, self.position = self.key_listener.get_position()

            self.menu.update_pointers(list_top, self.position)
            self.key_listener.set_max(len(self.menu))

            self.render_all()
            (
                selected['action'],
                selected['index'],
            ) = self.key_listener.get_action()

            if selected['action'] == 'help':
                self.help_bar.next_hint()
                selected['action'] = None
            if selected['action'] == 'expand':
                self.menu.expand_item(selected['index'])
                selected['action'] = None
            if _scroll_tab(selected['action']):
                if 'next' in selected['action']:
                    book = self.tabs.next_tab()
                else:
                    book = self.tabs.prev_tab()
                if book in self.books:
                    selected = {
                        'book': book,
                        'action': 'list',
                        'index': 0,
                    }
                else:
                    selected['action'] = None

        selected['item'] = self.menu.select_item(selected['index'])
        return selected


def _scroll_tab(action):
    return isinstance(action, str) and 'tab' in action
