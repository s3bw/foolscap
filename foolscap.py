
# import argparse

import sys
import os
from itertools import izip
from subprocess import call


from src.data_utils import save_data, note_data
from src.parse_utils import get_sections


def main(action, string_arg):
    whole_foolscap = note_data()
    
    if action == 'save':
        # loads notes into memory
        notepad = load_from_text(string_arg)

        # creates the notes into dict
        notepad = create_note_element(notepad)
        
        # combine to the larger notepad (saves)
        add_new_notes(notepad, old_data=whole_foolscap)

        
    if action == 'view':        
        # look for note
        view_note(whole_foolscap, string_arg)
        
        
    if action == 'list':
        list_all_notes(whole_foolscap)
        
        
    if action == 'edit':
        edited_note = edit_note(whole_foolscap, string_arg)
        
        edited_note = create_note_element(edited_note)
        
        overwrite_oldnote(edited_note, whole_foolscap)
        
        
    if action == 'delete':
        whole_foolscap.pop(string_arg, None)
        
        save_note_data(whole_foolscap)
    
    
if __name__ == '__main__':
    action = sys.argv[1]
    
    # file name should be optional
    file_name = sys.argv[2]
    
    main(action, file_name)
    
