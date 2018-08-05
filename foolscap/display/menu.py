import curses

from foolscap.display.menu_objects import MenuItem
from foolscap.display.menu_objects import Columns
from foolscap.display.render_composite import Widget


NORMAL_LINE_COLOUR = curses.A_NORMAL
DIM_LINE_COLOUR = curses.A_DIM
REVERSE_LINE_COLOUR = curses.A_REVERSE


def _set_colour(line, cursor):
    if line == cursor:
        return REVERSE_LINE_COLOUR
    if line % 2 == 0:
        return DIM_LINE_COLOUR
    return NORMAL_LINE_COLOUR


class MenuAdapter:
    """This object holds all the items in the list."""

    def __init__(self, items):
        """Get the data into the correct format.
        This should be handled before this"""
        self.menu = [MenuItem(**item) for item in items]

    @property
    def length(self):
        """Only counts the objects that are displayed."""
        length = sum([
            len(item.sub_items)
            for item in self.menu
            if hasattr(item, 'expand') and item.expand
        ]) + len(self.menu)
        return length

    def iter_viewable(self):
        """Yields the next appropriate item for the screen."""
        for item in self.menu:
            yield item
            if hasattr(item, 'expand') and item.expand:
                for sub_item in item.sub_items:
                    yield sub_item

    def iter_all(self):
        """Yields all menu items."""
        for item in self.menu:
            yield item
            if hasattr(item, 'expand'):
                for sub_item in item.sub_items:
                    yield sub_item


class DisplayMenu(Widget):
    """This object is responsible for displaying the menu."""

    def __init__(self, screen, items):
        model_type = items[0]['model'].model_type
        self.menu = MenuAdapter(items)
        #: available columns
        self.columns = Columns(model_type)
        self.columns.attach_screen(screen)
        self.attach_screen(screen)

    def __len__(self):
        """Length of menu list."""
        return self.menu.length

    def update_pointers(self, list_top, cursor):
        """Update the position of the cursor and the index to start
            drawing the menu items.

        :param int list_top: the index of the item that is at the top
            of the menu.
        :param int cursor: the position of the cursor.
        """
        #: items to skip before starting to draw
        self.reduction = list_top
        self.cursor = cursor

    def expand_item(self, expand_index):
        """Expand an item in the menu if it has sub items."""
        for index, item in enumerate(self.menu.iter_viewable()):
            if index == expand_index:
                if hasattr(item, 'sub_items'):
                    item.toggle_drop_down()

    def select_item(self, select_index):
        """Select an item in the menu."""
        for index, item in enumerate(self.menu.iter_viewable()):
            if index == select_index:
                if hasattr(item, 'start_index'):
                    return "{}@{}:{}".format(
                        item.parent_title,
                        item.start_index,
                        item.end_index
                    )
                else:
                    return item.title

    def draw_item(self, item):
        """Draw an item in the menu."""
        if self.reduction > 0:
            self.reduction -= 1
        else:
            self.draw_line += 1
            if self.draw_line < self.bottom_line - 1:
                line = self.draw_line
                line_colour = _set_colour(line, self.cursor)
                self.columns.draw(item, line, line_colour)

    def update(self):
        """Update the column object and screen."""
        self.columns.update()
        self.update_screen()

    def draw(self):
        """Draw all viewable menu items."""
        self.draw_line = self.top_line
        for item in self.menu.iter_viewable():
            self.draw_item(item)
