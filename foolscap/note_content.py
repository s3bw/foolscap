import os
import tempfile
from subprocess import call

from note_data import (
    save_data,
)

from parse_text import (
    load_text,
    note_component,
    shift_lines,
    update_component,
)


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
print(SCRIPT_DIR)
NOTE_STORAGE = '\\notes\\{note_name}.txt'
NOTE = SCRIPT_DIR + NOTE_STORAGE

RECYCLE_BIN = '\\deleted\\{note_name}.txt'
BIN = SCRIPT_DIR + RECYCLE_BIN

EDITOR = os.environ.get('EDITOR', 'vim')

NEW_NOTE_TEMPLATE = "# title\n==========\n: description\nMake sure you change the title!\n\n\n{tag}\n=========="


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
    """ Print the note to console if found.

    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        note_text = load_text(NOTE.format(note_name=note))
        
        for line in note_text:
            print(line)

    else:
        #Fuzzy here
        print('Not found')
       

def list_notes(tags, all_notes):
    # change template if more info is wanted
    # add config for changing list style

    if tags is not None:
        all_notes = { 
            key: values 
            for key, values in all_notes.items() 
            if 'tags' in values and tags in values['tags']
        }

    if len(all_notes) == 0:
        print("No note tagged with '{tag}'".format(tag=tags))
    
    basic_template = "+---> {title}\n"
    description_template = "   \\->  {description}\n"
    tags_template = " --  {tags}\n"
    
    for key, values in all_notes.items():
        if 'description' in values:
            print(basic_template.format(title=key), end=' ')
            print(description_template.format(description=values['description']))
            
            # if 'tags' in values:
                # print tags_template.format(tags=(' '.join(values['tags'])))
            
        else:
            print(basic_template.format(title=key))

            
def delete_note(note, stored_data):
    """ Delete a note stored in foolscap
    
    :param new_note: (string) name of .txt file.
    :param saved_notes: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        delete_file = NOTE.format(note_name=note)
        recycle_bin = BIN.format(note_name=note)
        d = 1

        while os.path.isfile(recycle_bin):
            recycle_bin = BIN.format(note_name='{} ({})'.format(note, str(d)))
            d += 1

        os.rename(delete_file, recycle_bin)

        stored_data.pop(note, None)
        save_data(stored_data)

    else:
        #Fuzzy here
        print('Not found')
            

def edit_note(note, stored_data):
    """ Edit the note from data in vim.
    
    :param note: (string) name of .txt file.
    :param stored_data: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    
    if note in stored_notes:
        edited_note = NOTE.format(note_name=note)
        
        with open(edited_note, 'r') as editing_text:
            editing_text.flush()
            call([EDITOR, editing_text.name])

        stored_data = update_component(note, stored_data)
        save_data(stored_data)
        
        print('Note updated')

    else:
        #Fuzzy here
        print('Not found')


def new_note(stored_notes):
    """ Create a new note in vim from template.

    :param stored_notes: (dict) of notes in data.
    """
    with tempfile.NamedTemporaryFile(mode='r+', suffix=".tmp") as new_text:
        new_text.write(NEW_NOTE_TEMPLATE)

        new_text.flush()
        call([EDITOR, new_text.name])
        new_text.seek(0)
        
        new_text = new_text.read().split('\n')

        # don't write unchanged notes.
        if '# title' != new_text[0]:
            new_component = note_component(new_text)
            stored_notes.update(new_component)
            save_data(stored_notes)
        else:
            print('Aborted New Note')


def move_lines(note, from_note, stored_data):
    """ Move selected lines from a note to another note.

    :parma note: (string) title of note to move lines to.
    :param from_note: (string) title of note to take lines from.
    :param stored_data: (dict) of notes in data.
    """
    stored_notes = stored_data.keys()
    if note not in stored_notes:
        print('{} not found.'.format(note))

    if from_note in stored_notes:
        edited_note = NOTE.format(note_name=from_note)
        
        with open(edited_note, 'r') as editing_text:
            editing_text.flush()
            call([EDITOR, editing_text.name])

        stored_data = shift_lines(from_note, note)
    else:
        print('{} not found.'.format(from_note))



