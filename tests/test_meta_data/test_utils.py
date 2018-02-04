import contextlib
from io import StringIO

from foolscap.meta_data.utils import fuzzy_guess


def test_fuzzy_guess():
    find_best = ['note', 'new', 'old']
    fake_input = 'nots'
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        fuzzy_guess(fake_input, find_best)
    output = temp_stdout.getvalue().strip()
    assert output == "Not found, did you mean \"note\"?"

