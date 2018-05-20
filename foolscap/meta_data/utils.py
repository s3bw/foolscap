from difflib import SequenceMatcher as SM
from collections import Counter, OrderedDict


NOT_FOUND = '\n\tNot found, did you mean "{}"?\n'


def fuzzy_guess(name, names):
    result = max(
        [
            (entry, SM(None, name, entry).ratio())
            for entry in names
        ],
        key=lambda x: x[1]
    )
    print(NOT_FOUND.format(result[0]))


class OrderedCounter(Counter, OrderedDict):
    pass
