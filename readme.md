# Foolscap Note Manager

![build](https://travis-ci.org/GiantsLoveDeathMetal/foolscap.svg?branch=master) 

The foolscap note manager allows a user to track and maintain notes over many topics.

## Install:

To install foolscap do the following:

    git clone git@github.com:GiantsLoveDeathMetal/foolscap.git
    cd foolscap
    pip install .
    
Then you'll need to set the `FSCAP_PATH` environment variable:

    export FSCAP_PATH=~/.fscap_notes
    
Lastly create the following directories:

    mkdir ~/.fscap_notes
    mkdir ~/.fscap_notes/data
    mkdir ~/.fscap_notes/notes
    mkdir ~/.fscap_notes/deleted

---

## Preview:

[![asciicast](https://asciinema.org/a/L7HTfOt02pBDvCBxWme9CxBYV.png)](https://asciinema.org/a/L7HTfOt02pBDvCBxWme9CxBYV)

## Note Structure:

Please take care, the following documentation is intentionally outdated while `foolscap` is in Alpha.

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

#### title_of_note:

The note should contain a title, identified with `#` at the start of the line. The title can be changed at a later point but this will be the primary-key to the note should you want to manipulate it using foolscap.

#### note content:

The note should be encapsulated by '==' on the first line after the title and directly after your tags. Anything that falls outside the note boundaries will not be saved.

#### :The note description

This falls directly below the start line of the note. This should capture a little more detail on your note. This is an optional feature, but allows an easier reminder of the contents of the note.

#### {tags}

The tags should be place on the last line of the note before the note's line ending. These tags allow for filtering by tag when searching for notes.

---

## Using Foolscap:

Below is a breakdown of the features that foolscap encaptulate:

#### Saving:

To save a note that has been written to a `.txt` one can use the following command:

    fscap save my_note.txt

Multiple notes in one `.txt` will be separated into different notes.

#### List:

The list function allows the user to view their contained notes. The description is also accompanied to the note title in the list.

    fscap list

If you want to filter notes by a specific tag all one has to do is append the tag to the command line:

    fscap list <tag>

More options on the list function will be included in up coming features.

#### View:

The `view` command allows the user to view a note in the console. To call function use the following:

    fscap view <note_title>

The note title should be the second positional argument in this case.

#### Edit:

The `edit` command allows a user to open their notes in the `vim` editor to make changes and foolscap will append the changes after closing.

    fscap edit <note_title>

After making changes to the note close `vim` with the `:wq` command and foolscap will update the note.

#### Delete:

To delete a note, type command:

    fscap delete <note_title>


#### New Note:

To create a new note from a default note template, type command:

    fscap new


#### Move lines across notes:

Foolscap allows you to move lines from one note to another using the `move-to` command:

    fscap move_lines <note_title>

Then you will be prompted for the note you want to take the lines from, enter the title of the note you'd like to take lines from. This should open a vim editor, specify the lines you'd like to move with `>` at the beginning of each line.
