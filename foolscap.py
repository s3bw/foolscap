"""
# Add notes to foolscap
# find notes by header (display header)
    - show contents

# foolscap.py =status
        --> some note taking stats 
    
|X|# foolscap.py -s (-save) note.txt 
    |X| save the txt to directory
    |X| txt might contain multiple notes
    |X| txt note might already exist, get to suggest a new name
    --? dict should contain timestamps (last viewed and created)
    
|X| # foolscap.py -ls (--list)
    |X| --> list all notes
    
# foolscap.py -r (--rename ) notes_on_stuff outline_of_doc_process
    --> rename notes heading to something more descriptive
    
|X| # foolscap.py note -d
    |X| --> delete the note from foolscap

|X| # foolscap.py -v (--view) windows_notes
    |X| --> returns the notes if found
    --> if its not found fuzzy match string onto notes and return top 3.
    
|X| # foolscap.py -e windows_notes
    |X| --> opens vim instance of notes for editing
    --> if its not found fuzzy match string onto notes and return top 3.
    
# identify if they are meeting notes for other options 
    --? meeting notes with attendees

# foolscap.py -m (--merge) note_1 note_2 
        --> append 2 to 1 and delete 2.
        --> make notes smallers
    
# foolscap.py -export note
    --> save note as note.txt
    
# foolscap.py -n -new 
        --> creates a new note from scratch
    
    
"""


# import argparse

import sys
import pickle
from itertools import izip

import os
from subprocess import call


def save_note_data(data):
    """ Save the data dict to file.

    :param data: (dict) containing all notes.
    """
    with open('data/note_data.pkl', 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def load_note_data():
    """ Load the note data into a dict.
    """
    try:
        with open('data/note_data.pkl', 'rb') as _input:
            return pickle.load(_input)
    except EOFError and IOError:
        return {}
        

def load_from_text(text):
    with open(text) as notes:
        notes = notes.read()
        return notes.split('\n')


def overwrite_oldnote(edited_note, old_data):
    print 'overwritten'
    old_data.update(edited_note)
    
    
    save_note_data(old_data)

        
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

    
def get_sections(note):
    sections = [line[2:] for line in note if line[:2] == '# ']
    return sections
    
    
def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)
    
    
def get_contents(note):
    content_index = [index for index, line in enumerate(note) if line[:2] == '==']
    
    number_of_notes = len(content_index) / 2
    
    content_list = []
    indexes = pairwise(content_index)
    
    for start, end in indexes:
        content = note[start:end+1]
        content_list.append(content)
        
    return content_list
    
    
def create_note_element(note):
    """ Creates the new note data structure.
        Here is where one would add more note information.
        
    :param note: (list) of string containing a single note.
    :return: the dict note element.
    """
    sections = get_sections(note)
    contents = get_contents(note)
    
    #print sections, contents
    
    note_element = {}
    for section, content in zip(sections, contents):
    
        note_element[section] = {
            'content':None, 
            'timestamp':None,
        }
        
        note_element[section]['content'] = content
        note_element[section]['timestamp'] ='now'
        
        description = content[1]
        if description and description[0] == ':':
            note_element[section]['description'] = description
        
            
    return note_element
    
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
        

def main(action, string_arg):
    whole_foolscap = load_note_data()
    
    
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
    
