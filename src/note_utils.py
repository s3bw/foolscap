import os
from subprocess import call

from data_utils import (
    save_data,
)

from parse_utils import (
    load_text,
    note_component,
    update_component,
)


NOTE_DIR = 'notes/{note_name}.txt'
EDITOR = os.environ.get('EDITOR', 'vim')


def save_note(new_note, saved_notes):
    """ Convert note.txt to dict components and save.
    
    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    new_note = load_text(new_note)
    new_component = note_component(new_note)
        
    saved_notes.update(new_component)
    save_data(saved_notes)
    
    
def view_note(note, stored_data):
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        note_text = load_text(NOTE_DIR.format(note_name=note))
        
        for line in note_text:
            print line
        # iterate the views
    else:
        #Fuzzy here
        print 'Not found'
       

def list_notes(all_notes):
    # change template if more info is wanted
    # add config for changing list style
    basic_template = "+---> {title}\n"
    description_template = "+---> {title}: \n  \\->{description}\n"
    
    # print descriptions
    print '\n'
    for key, values in all_notes.items():
        if 'description' in values:
            print description_template.format(title=key, description=values['description'])
        else:
            print basic_template.format(title=key)

            
def delete_note(note, stored_data, recycle=True):
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        delete_file = NOTE_DIR.format(note_name=note)
        recycle_bin = 'deleted/{note_name}.txt'.format(note_name=note)
        
        os.rename(delete_file, recycle_bin)

        stored_data.pop(note, None)
        save_data(stored_data)

    else:
        #Fuzzy here
        print 'Not found'
            

def edit_note(note, stored_data):
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        edited_note = NOTE_DIR.format(note_name=note)
        
        with open(edited_note, 'r') as editing_text:
            editing_text.flush()
            call([EDITOR, editing_text.name])


        stored_data = update_component(note, stored_data)
        save_data(stored_data)
        
        print 'Note updated'

    else:
        #Fuzzy here
        print 'Not found'

        