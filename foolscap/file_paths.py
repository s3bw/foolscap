import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# data/note_data.pkl.
DATA_STORAGE = os.path.join('data', 'note_data.pkl')
NOTE_DATA = os.path.join(SCRIPT_DIR, DATA_STORAGE)

NOTE_STORAGE = os.path.join('notes', '{note_name}.txt')
NOTES = os.path.join(SCRIPT_DIR, NOTE_STORAGE)

RECYCLE_BIN = os.path.join('deleted', '{note_name}.txt')
BIN = os.path.join(SCRIPT_DIR, RECYCLE_BIN)

NOTE_DIR = 'notes'
NOTE_DIR = os.path.join(SCRIPT_DIR, NOTE_DIR)
