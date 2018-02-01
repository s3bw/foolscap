





def remove_moving_lines(note):
    _lines = [line for line in note if line[:1] != '>']
    return _lines





def shift_lines(name_from_note, name_to_note):
    # load text, return note, delete, save new
    take_from_note = load_text(path_from)
    remove_text(path_from)

    replace_note = get_contents(take_from_note)[0]
    replace_note = remove_moving_lines(replace_note)
    save_text(name_from_note, replace_note)

    # load text, return note, apply new, delete old, save new
    apply_to_note = load_text(name_to_note)
    # Get contents with be tricky to refactor
    apply_to_note = get_contents(apply_to_note)[0]

    line_index = len(apply_to_note) - 2
    # Insert moved lines into other note.
    apply_to_note[line_index:line_index] = get_moving_lines(take_from_note)
    remove_text(name_to_note)
    save_text(name_to_note, apply_to_note)


