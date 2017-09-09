import os
from itertools import izip


NOTES_DIRECTORY = "notes/"


def load_text(text):
    with open(text) as notes:
        notes = notes.read()
        return notes.split('\n')
        
        
def unique_note(heading):
    saved_notes = [x[:-4] for x in os.listdir(NOTES_DIRECTORY)]

    suffix = 0
    if heading in saved_notes:
        while '{}_{}'.format(heading, str(suffix)) in saved_notes:
            suffix += 1
        new_name = '{}_{}'.format(heading, str(suffix))
        heading = new_name
        
    return heading
        
        
def save_text(heading, content):
    heading = unique_note(heading)
    
    text_string =  '\n# {heading}\n'.format(heading=heading)
    for line in content:
        text_string += '{}\n'.format(line)
        
    name_note = '{note_dir}{heading}.txt'.format(
        note_dir=NOTES_DIRECTORY,
        heading=heading
    )
    
    with open(name_note, 'w') as save_txt:
        save_txt.write(text_string)
        
    return heading
    

def get_sections(note):
    _sections = [line[2:] for line in note if line[:2] == '# ']
    return _sections
    
    
def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)
    
    
def note_description(content):
    """"        """
    description = content[1]
    if description and description[0] == ':':
        return description
    return None

    
def note_tags(contents):
    """         """
    tag_line = contents[-1]
    if tag_line and '{' in tag_line:
        return tag_line.split(' ')
    return None
    
    
def get_contents(note):
    content_index = [index for index, line in enumerate(note) if line[:2] == '==']
    
    number_of_notes = len(content_index) / 2
    
    content_list = []
    indexes = pairwise(content_index)
    
    for start, end in indexes:
        content = note[start:end+1]
        content_list.append(content)
        
    return content_list

    
def note_component(note):
    """ Creates the new note data structure.
        Here is where one would add more note information.
        
    :param note: (list) of string containing a single note.
    :return: the dict note element.
    """
    sections = get_sections(note)
    contents = get_contents(note)
    
    
    note_component = {}
    for heading, content in zip(sections, contents):
        heading = save_text(heading, content)
    
        note_component[heading] = {
            'timestamp':None,
        }
        
        note_component[heading]['timestamp'] ='now'
        
        description = note_description(content)
        if description:
            note_component[heading]['description'] = description
            
        tags = note_tags(content)
        if tags:
            note_component[heading]['tags'] = tags
            
        
    return note_component
