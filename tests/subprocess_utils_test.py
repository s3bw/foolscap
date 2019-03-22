import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap import subprocess_utils


class FileObject(MagicMock):
    @property
    def name(self):
        return 'note.txt'


@pytest.mark.parametrize(
    "case, expected",
    [(None, ['vim', '+set backupcopy=yes', 'note.txt']),
     (
         ':set textwidth=30',
         ['vim', '-c', ':set textwidth=30', '+set backupcopy=yes', 'note.txt'],
     )])
def test_edit_in_vim(case, expected):
    _file = FileObject()
    with patch('foolscap.subprocess_utils.call') as mock_call:
        subprocess_utils.edit_in_vim(_file, add_cmds=case)

    mock_call.assert_called_with(expected)
    assert _file.mock_calls == [call.flush()]
