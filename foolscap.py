import sys
import os

from src.data_utils import note_data
from src.note_utils import (
    save_note,
    view_note,
    list_notes,
    delete_note,
    edit_note,
)


def main(action, note):
    whole_foolscap = note_data()
    
    if action == 'save' or action == '-s':
        notepad = save_note(note, whole_foolscap)

        
    if action == 'view' or action == '-v':
        view_note(note, whole_foolscap)
        
    # list only those containing a tag
    if action == 'list' or action == 'ls':
        list_notes(whole_foolscap)
        
        
    if action == 'delete' or action == '-d':
        delete_note(note, whole_foolscap)

    if action == 'edit' or action == '-e':
        edited_note = edit_note(note, whole_foolscap)
        
    print '{} {}'.format(note, action)
        
    
    
if __name__ == '__main__':
    action = sys.argv[1]
    
    # file name should be optional
    file_name = sys.argv[2]
    
    main(action, file_name)
    
