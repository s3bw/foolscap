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


def main(action, note, filter_tags):
    whole_foolscap = note_data()
    
    if action == 'save' or action == '-s':
        notepad = save_note(note, whole_foolscap)

        
    if action == 'view' or action == '-v':
        view_note(note, whole_foolscap)
        

    if action == 'list' or action == 'ls':
        list_notes(filter_tags, whole_foolscap)
        
        
    if action == 'delete' or action == '-d':
        delete_note(note, whole_foolscap)


    if action == 'edit' or action == '-e':
        edited_note = edit_note(note, whole_foolscap)


    print 'Action called {}'.format(action)
        
    
    
if __name__ == '__main__':
    file_name = None

    action = sys.argv[1]
   
    # list has more complex functionality. 
    # With flags for list type and tags for filtering

    # We could probably do this better by picking and removing flags
    # from the list

    filter_tags = None

    if action == 'list' or action == 'ls':
        if len(sys.argv) > 2:
            if '-' ==  sys.argv[2][0]:
                flag = sys.argv[2]

                if len(sys.argv) > 3:
                    filter_tags = sys.argv[3]

            else:
                filter_tags = sys.argv[2]

    else:
        file_name = sys.argv[2]


    main(action, file_name, filter_tags)
    
