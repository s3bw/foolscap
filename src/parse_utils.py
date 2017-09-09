



def load_from_text(text):
    with open(text) as notes:
        notes = notes.read()
        return notes.split('\n')
        
def sections(note):
    _sections = [line[2:] for line in note if line[:2] == '# ']
    return _sections
    
    
def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)
    
    
def contents(note):
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
    sections = sections(note)
    contents = contents(note)
    
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