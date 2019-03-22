import os
from subprocess import call


EDITOR = os.environ.get('EDITOR', 'vim')


def edit_in_vim(open_file, add_cmds=None):
    """Open the file object in Vim.

    :param File open_file: file object.
    :param str add_cmds: additional vim commands:
    """
    open_file.flush()
    cmd = [EDITOR, "+set backupcopy=yes", open_file.name]
    if add_cmds:
        cmd = [EDITOR, '-c', add_cmds, "+set backupcopy=yes", open_file.name]

    call(cmd)

