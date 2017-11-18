

def list_notes(tags, all_notes):
    
    if tags:
        all_notes = {
            key: values
            for key, values in all_notes.items()
            if 'tags' in values and tags in values['tags']
        }

    if len(all_notes) == 0:
        print("No note tagged with '{tag}'".format(tag=tags))

    basic_template = "+---> {title}\n"
    description_template = "    \\->  {description}\n"
    # tags_template = " -- {tags}\n"

    # Below for loop should move to cli
    for key, values in all_notes.items():
        if 'description' in values:
            print(basic_template.format(title=key), end=' ')
            print(
                description_template.format(
                    description=values['description']
                )
            )

            # if 'tags' in values:
            # print tags_template.format(tags=(' '.join(values['tags'])))

        else:
            print(basic_template.format(title=key))



