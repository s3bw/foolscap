from datetime import date

from foolscap.meta_data.io import load_tag_history
from foolscap.meta_data.io import save_tag_history


TAG_HISTORY = 50
DELETION_STYLE = "{{{tag}}} -remove-from- {note} {date}"
ADDITION_STYLE = "{{{tag}}} +added+to+ {note} {date}"


class TagsHistory(list):

    def __init__(self):
        self.extend(load_tag_history())

    def _deprecate_lines(self, delta):
        """Determines the amount of history to deprecate."""
        lines = 0
        if len(self) + delta > TAG_HISTORY:
            lines = len(self) + delta - TAG_HISTORY
        return lines

    def check_deprecation(self, delta):
        """Set number of lines in history to deprecate."""
        self.deprecate_lines = self._deprecate_lines(delta)

    def save(self):
        save_tag_history(self, self.deprecate_lines)


def format_new_history(style, note, new_history):
    """Style the format of each tag history entry.

    :param str style: format string for history entries.
    :param str note: name of note being changed.
    :param list[str] new_history: entries to be added to log.
    """
    now = date.today().strftime("%Y-%m-%d")
    return [
        style.format(tag=new, note=note, date=now)
        for new in new_history
    ]


def record_tags(note, deleted, added):
    """Record changes to tags history.

    :param str note: name of note being changes.
    :param list deleted: a list of deleted tags.
    :param list added: a list of added tags.
    """
    history = TagsHistory()

    deletions = format_new_history(DELETION_STYLE, note, deleted)
    additions = format_new_history(ADDITION_STYLE, note, added)

    n_changes = len(deleted | added)

    history.check_deprecation(n_changes)
    history += deletions + additions
    history.save()


def diff_tags(current_tags, previous_tags, note_name):
    """Checks for changes in tags and records these changes.

    :param list current_tags: a list of current tags.
    :param list previous_tags: a list of the previous tags.
    :param str note_name: name of note being changed.
    """
    deleted = set(previous_tags) - set(current_tags)
    added = set(current_tags) - set(previous_tags)

    record_tags(note_name, deleted, added)
