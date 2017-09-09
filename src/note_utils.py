
from data_utils import (
    save_data,

)

from parse_utils import (
    load_text,
    note_component,
)

        
def save_note(new_note, saved_notes):
    """ Convert note.txt to dict components and save.
    
    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    new_note = load_text(new_note)
    new_component = note_component(new_note)
        
    saved_notes.update(new_component)
    save_data(saved_notes)
    
    
def view_note(stored_data, note):
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        text_file = 'notes/{file_name}.txt'
        note_text = load_text(text_file.format(file_name=note))
        
        for line in note_text:
            print line
        
    else:
        #Fuzzy here
        print 'Not found'
       

def list_notes(all_notes):
    # change template if more info is wanted
    # add config for changing list style
    basic_template = "+---> {title}\n"
    description_template = "+---> {title}: \n  ->{description}\n"
    
    # print descriptions
    print '\n'
    for key, values in all_notes.items():
        if 'description' in values:
            print description_template.format(title=key, description=values['description'])
        else:
            print basic_template.format(title=key)
            
            
def overwrite_oldnote(edited_note, old_data):
    print 'overwritten'
    old_data.update(edited_note)
    save_data(old_data)





def edit_note(note, key):
    EDITOR = os.environ.get('EDITOR', 'vim')
    text_string =  '\n# {heading}\n'.format(heading=key)
    
    try:
        for line in note[key]['content']:
            text_string += '{}\n'.format(line)
            
        with open("editing.txt", 'w') as tf:
            tf.write(text_string)
            tf.flush()
            call([EDITOR, tf.name])

            with open(tf.name) as edited_file:                
                edited_message = edited_file.read()
    
        print edited_message
        return edited_message.split('\n')
        
        
    except KeyError:
        #Fuzzy here
        print 'No such note saved'
        
        
        
        