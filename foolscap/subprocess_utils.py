import os
from subprocess import call

EDITOR = os.environ.get('EDITOR', 'vim')

def edit_in_vim(open_file):
    open_file.flush()
    call([EDITOR, open_file.name])

