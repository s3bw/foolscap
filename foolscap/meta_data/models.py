from foolscap.meta_data.io import load_meta
from foolscap.meta_data.utils import fuzzy_guess
from foolscap.meta_data.utils import OrderedCounter


class Model:

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    @property
    def model_type(self):
        raise NotImplementedError

    def get(self, item):
        raise NotImplementedError

    def filter_by_value(self, items, key, value):
        return items


class NotesModel(Model):

    model_type = 'notes'

    def __init__(self):
        self.notes = load_meta()

        self.tags = [values['tags'] for _, values in self.notes.items()]
        self.tags = [n for x in self.tags for n in x]

        self.books = [values['book'] for _, values in self.notes.items()]

    def __iter__(self):
        for item in self.notes:
            yield item

    def __len__(self):
        return len(self.notes)

    def get(self, item):
        try:
            return self.notes[item]
        except KeyError:
            fuzzy_guess(item, self.notes.keys())

    def get_value(self, item, value_key):
        return self.notes[item].get(value_key, None)

    def filter_by_value(self, items, key, value):
        return [item
                for item in items
                if self.get_value(item, key) == value]

    def query_tags(self, tag):
        titles = [title
                  for title, values in self.notes.items()
                  # Check if I can use self.get_value here?
                  if 'tags' in values and tag in values['tags']]
        if titles:
            return titles
        fuzzy_guess(tag, self.tags)

    def query_titles(self, query):
        try:
            search = [title
                      for title, values in self.notes.items()
                      if query in title]

            # Sort by the position the query appears in the title
            titles = sorted(search, key=lambda title: title.index(query))

        except TypeError:
            raise TypeError("Invalid Query")
        if titles:
            return titles
        self.get(query)


class TagsModel(Model):

    model_type = 'tags'

    def __init__(self, notes):
        tags = OrderedCounter(notes.tags).most_common()
        tags = [
            (
                tag,
                str(count),
                [(title, notes.get_value(title, 'description'))
                 for title in notes.query_tags(tag)]
            )
            for tag, count in tags
        ]
        self.tags = {
            tag: {
                'title': tag,
                'description': count,
                # Title are sorted alphabetically
                'sub_headings': sorted(titles,
                                       key=lambda x: x[0].lower())
            }
            for tag, count, titles in tags
        }
        self.books = notes.books

    def __iter__(self):
        for item in self.tags:
            yield item

    def __len__(self):
        return len(self.tags)

    def get(self, tag):
        try:
            return self.tags[tag]
        except KeyError:
            fuzzy_guess(tag, self.tags.keys())

    def get_value(self, item, info):
        return self.tags[item].get(info, None)

    def query_tags(self, query):
        tags = [
            tag
            for tag, _ in self.tags.items()
            if tag.startswith(query)
        ]
        if tags:
            return tags
        self.get(query)

    def query_titles(self, query):
        try:
            titles = [title
                      for title, values in self.tags.items()
                      if title.startswith(query)]
        except TypeError:
            raise TypeError("Invalid Query")
        if titles:
            return titles
        self.get(query)

