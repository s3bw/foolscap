from difflib import SequenceMatcher as SM


def fuzzy_guess(name, names):
    result = max(
        [
            (entry, SM(None, name, entry).ratio())
            for entry in names
        ],
        key=lambda x: x[1]
    )
    return result[0]
