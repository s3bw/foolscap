from foolscap.backend.api import API

_NOTE_ID = 'fake_note'


api = API(protocol='http://', host='localhost:5000')

note = api.get_note_content(_NOTE_ID)
print(note)

note = api.get_note_json(_NOTE_ID)
print(note)
