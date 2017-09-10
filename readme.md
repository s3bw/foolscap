# Foolscap Note Manager

The foolscap note manager allows a user to track and maintain notes over many topics.

---

## Note Writting:

There are several key features that should be included into the note in order for it to be parsed into the foolscap data collector.

A typical note should contain the following:


    # title_my_note
    ===============
    : Here is a description of what the note contains
    I can begin typing out notes
        - one topics
        - as a check list
        - etc
    
    {checklist} {code} {tags}
    ================

#### title_of_note

The note should contain a title, this can be changed at a later point but this will be the key hook to the note should you want to manipulate it using foolscap.

#### note start and end.

The note should be encaptulated by '==' on the first line after the title and directly after your tags. Anything that falls outside the note boundaries will not be saved.

#### :The note description

This falls directly below the start line of the note. This should capture a little more detail on your note. This is an optional feature, but allows an easier reminder of the contents of the note.

#### {tags}

The tags should be place on the last line of the note before the note's line ending. These tags allow for filtering by tag when searching for notes.

---

## Using Foolscap:

Below is a breakdown of the features that foolscap encaptulate:

#### Saving:

To save a note that has been written to a `.txt` one can use the following command:

    python foolscap.py save my_note.txt

save can be substituted for `-s`

Multiple notes in one `.txt` will be separated into different notes.

#### List:

The list function allows the user to view their contained notes. The description is also accompanied to the note title in the list.

    python foolscap.py ls

If you want to filter notes by a specific tag all one has to do is append the tag to the command line:

    python foolscap.py ls code

More options on the list function will be included in up coming features.

#### View:

The `view/-v` command allows the user to view a note in the console. To call function use the following:

    python foolscap.py view my_note

The note title should be the second positional argument in this case.

#### Edit:

The `edit/-e` command allows a user to open their notes in the `vim` editor to make changes and foolscap will append the changes after closing.

    python foolscap.py edit my_note

After making changes to the note close `vim` with the `:wq` command and foolscap will update the note.

---

### Future Changes:

These are the features that planned in the future of foolscap:

    - rename. To rename the notes saved in foolscap.
    - list options. To allow for a custom functioning of the list output.
    - merge. To merge two notes into one.
    - split. To split one note into two.
    - multiple descriptions. To allow one note be broken into sections.
    - export. To allow the output of a note be exported in various ways.
    - config. To allow a user to change the foolscap-markup of titles and descriptions.














