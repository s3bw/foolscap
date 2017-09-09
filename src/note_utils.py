

def overwrite_oldnote(edited_note, old_data):
    print 'overwritten'
    old_data.update(edited_note)
    save_note_data(old_data)

def view_note(note, key):
    print '\n# {heading}'.format(heading=key)
    
    try:
        for line in note[key]['content']:
            print line
    except KeyError:
        #Fuzzy here
        print 'No such note saved'


def list_all_notes(all_notes):
    # change template if more info is wanted
    basic_template = "--{title}\n"
    description_template = "--{title}: \n    {description}\n"
    
    # print descriptions
    print '\n'
    for key, values in all_notes.items():
        if 'description' in values:
            print description_template.format(title=key, description=values['description'])
        else:
            print basic_template.format(title=key)
            
            
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
        
def add_new_notes(new_notes, old_data):
    new_sections = new_notes.keys()
    old_sections = old_data.keys()
    
    for section in new_sections:
        suffix = 0
        if section in old_sections:
            while '{}_{}'.format(section, str(suffix)) in old_sections:
                suffix += 1
            new_name = '{}_{}'.format(section, str(suffix))
            new_notes[new_name] = new_notes[section]
            new_notes.pop(section, None)
    
    old_data.update(new_notes)
    save_note_data(old_data)
        
        
        
        