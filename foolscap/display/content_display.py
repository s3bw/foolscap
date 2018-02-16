import curses

from foolscap.display.root_screen import Terminal
from foolscap.display.content import MenuItem
from foolscap.display.content import SubItem


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE

TITLE = "|>  {}"
SUB_TITLE = "|   > {}"
DESCRIPTION = "  {}"
EXPANDABLE = "+ {}"
EXPANDED = "\->{}"


def _set_colour(line, cursor):
    if line == cursor:
        return REVERSE_LINE_COLOUR
    if line % 2 == 0:
        return DIM_LINE_COLOUR
    return NORMAL_LINE_COLOUR


# This is probably two Classes
# - Render Menu
# - Menu
class DisplayContents(Terminal):
    def __init__(self, screen, items):
        Terminal.__init__(self, screen)
        self.menu_items = self.build_menu(items)

    def expand(self, expand_index=None):
        if expand_index:
            expand_item = self.menu_items[expand_index - 1]
            if hasattr(expand_item, 'sub_items'):
                self.menu_items[expand_index - 1].toggle_drop_down()
                self.menu_items = self.update_menu()
        return self.menu_items

    def update_menu(self):
        new_menu = []
        for item in self.menu_items:
            if not isinstance(item, SubItem):
                new_menu.append(item)
            if hasattr(item, 'sub_items') and item.expand:
                for sub in item.sub_items:
                    new_menu.append(sub)
        return new_menu

    def build_menu(self, items):
        menu_items = []
        for item in items:
            title = item['title']
            description = item['description']
            if 'sub_headings' in item.keys():
                sub_item = item['sub_headings']
            else:
                sub_item = None
            menu_item = MenuItem(title, description,
                                 sub_item)
            menu_items.append(menu_item)
        return menu_items

    def update_pointers(self, first_index, cursor):
        self.first_index = first_index
        self.cursor = cursor

    def find_next_item(self, index):
        item = self.menu_items[index]
        while isinstance(item, SubItem):
            index += 1
            # if needs to be tested
            if index >= len(self.menu_items):
                return None, index
            item = self.menu_items[index]
        return self.menu_items[index], index

    def draw_item(self, line, col_1, col_2):
        line_colour = _set_colour(line, self.cursor)
        self.screen.addstr(line, 0, col_1, line_colour)
        if self.max_x > 64:
            self.screen.addstr(line, self.centre_x - 2,
                               col_2, line_colour)

    def draw(self):
        """
        'top_note' first note in list
        """
        index_item = self.first_index
        draw_line = self.top_line + 1
        while draw_line < self.bottom_line - 1:
            if index_item >= len(self.menu_items):
                break

            item, index_item = self.find_next_item(index_item)
            if item and hasattr(item, 'sub_items'):
                self.draw_item(draw_line,
                               TITLE.format(item.title),
                               EXPANDABLE.format(item.desc))
                if item.expand:
                    for sub in item.sub_items:
                        draw_line += 1
                        self.draw_item(draw_line,
                                       SUB_TITLE.format(sub.title),
                                       EXPANDED.format(sub.desc))

            elif item:
                self.draw_item(draw_line,
                               TITLE.format(item.title),
                               DESCRIPTION.format(item.desc))

            draw_line += 1
            index_item += 1



