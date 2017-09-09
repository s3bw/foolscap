
# import argparse

import sys
import os

from subprocess import call


from src.data_utils import save_data, note_data

from src.note_utils import (
    save_note,
    view_note,
    list_notes,
)



def main(action, note):
    whole_foolscap = note_data() # Have this run an update on data
    
    
    if action == 'save':
        notepad = save_note(note, whole_foolscap)

        
    if action == 'view':
        view_note(whole_foolscap, note)
        
        
    if action == 'list':
        list_notes(whole_foolscap)
        
        
    if action == 'delete':
        whole_foolscap.pop(string_arg, None)
        save_note_data(whole_foolscap)
        
        
    if action == 'edit':
        edited_note = edit_note(whole_foolscap, string_arg)
        
        edited_note = create_note_element(edited_note)
        
        overwrite_oldnote(edited_note, whole_foolscap)
        
        
    
    
if __name__ == '__main__':
    action = sys.argv[1]
    
    # file name should be optional
    file_name = sys.argv[2]
    
    main(action, file_name)
    
