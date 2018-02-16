class MenuItem:
    def __init__(self, title, desc, sub_headings):
        self.title = title
        self.desc = desc
        if sub_headings:
            self.expand = False
            self.create_sub_items(sub_headings)

    def toggle_drop_down(self):
        if self.sub_items:
            self._toggle_dd()

    def _toggle_dd(self):
        if self.expand:
            self.expand = False
        else:
            self.expand = True

    def create_sub_items(self, items):
        self.sub_items = []
        for i in items:
            sub_item = SubItem(i)
            self.sub_items.append(sub_item)


class SubItem:
    def __init__(self, unpack):
        title, desc = unpack
        self.title = title
        self.desc = desc
