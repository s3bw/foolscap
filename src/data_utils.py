import pickle



def save_data(data):
    """:param data: (dict) containing all notes."""
    with open('data/note_data.pkl', 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def note_data():
    """ Load the note data into a dict."""
    try:
        with open('data/note_data.pkl', 'rb') as _input:
            return pickle.load(_input)
    except EOFError and IOError:
        return {}
        
        
        
        