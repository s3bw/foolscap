from mock import patch
from mock import Mock

import foolscap.fuzzy_note as fuzzy


def test_fuzzy_guess():
    find_best = ['note', 'new', 'old']
    fake_input = 'nots'
    result = fuzzy.fuzzy_guess(fake_input, find_best)
    
    assert result == 'note'


