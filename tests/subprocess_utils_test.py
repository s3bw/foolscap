import pytest
from mock import call
from mock import patch
from mock import MagicMock

from foolscap import subprocess_utils


class FileObject(MagicMock):

    @property
    def name(self):
        return 'note.txt'


@pytest.mark.parametrize("cmds, expected",
    [
        (None, ['vim', 'note.txt']),
        (
            ':set textwidth=30',
            ['vim', '-c', ':set textwidth=30', 'note.txt'],
        )
    ]
)
def test_edit_in_vim(cmds, expected):
    _file = FileObject()
    with patch('foolscap.subprocess_utils.call') as mock_call:
        subprocess_utils.edit_in_vim(_file, add_cmds=cmds)

    mock_call.assert_called_with(expected)
    assert _file.mock_calls == [call.flush()]
