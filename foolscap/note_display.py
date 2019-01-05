from foolscap.meta_data import TagsModel
from foolscap.meta_data import NotesModel
from foolscap.meta_data.utils import fuzzy_guess
from foolscap.display.console import display_list


class Controller:

    def __init__(self, model_type):
        self.model = NotesModel()
        if model_type == 'tags':
            self.model = TagsModel(self.model)
        self.service_rules = ServiceRules(self.model)

    def __service_rules(self, items, tab_title):
        items = self.service_rules.order(items)
        structure = self.service_rules.structure(items)
        structure['tab_title'] = tab_title
        return display_list(structure)

    def basic_output(self, book):
        items = list(self.model)
        self.items = self.service_rules.filter_items(items, book)
        return self.__service_rules(self.items, book)

    def query_output(self, query):
        items = self.model.query_tags(query)
        if not items:
            exit()
        return self.__service_rules(items, "tag: '{}'".format(query))

    def search_output(self, query):
        if not query:
            print("\n\tNo Query Error\n")
            exit()
        items = self.model.query_titles(query)
        if not items:
            exit()
        structure = self.service_rules.structure(items)
        structure['tab_title'] = 'search'
        return display_list(structure)


class ServiceRules:

    ORDER_RULE = 5
    FILTER_RULE = 10
    TOP_N_VIEWED = 3

    def __init__(self, model):
        self.model = model

    def order(self, items):
        if self.model.model_type == 'tags':
            return self.by_count(items)
        return self.order_notes(items)

    def filter_items(self, items, book):
        if len(items) > self.FILTER_RULE:
            books = self.model.books
            try:
                books.index(book)
                return self.model.filter_by_value(
                    items,
                    'book',
                    book,
                )
            except ValueError:
                fuzzy_guess(book, books)
                exit()
        return items

    def order_notes(self, items):
        if len(items) > self.ORDER_RULE:
            return self.clever_order(items)
        return self.by_views(items)

    def clever_order(self, items):
        """
        - last opened unless in top 3 most viewed
        - N most viewed
        - A to Z
        """
        viewed = self.by_views(items)
        viewed, items = (viewed[:self.TOP_N_VIEWED],
                         viewed[self.TOP_N_VIEWED:])

        recent = self.last_viewed(items)
        recent, items = (recent[:1], recent[1:])

        return recent + viewed + self.alphabetise(items)

    def alphabetise(self, iterable):
        return sorted(iterable, key=lambda x: x.lower())

    def last_viewed(self, iterable):
        def sort_key(x):
            return self.model.get_value(x, 'modified')
        return sorted(iterable,
                      key=sort_key,
                      reverse=True)

    def by_views(self, iterable):
        """ Sorts by views then sorts alphabetically.
        """
        def sort_key(x):
            return (-self.model.get_value(x, 'views'), x.lower())
        return sorted(iterable,
                      key=sort_key)

    def by_count(self, iterable):
        def sort_key(x):
            return int(self.model.get_value(x, 'description'))
        return sorted(iterable,
                      key=sort_key,
                      reverse=True)

    def structure(self, iterable):
        return {
            'titles': [item for item in iterable],
            'model': self.model,
            'books': self.model.books,
        }
