def extract_intro(filename):
    """ Extract the first paragraph of module-level docstring. max:95 char"""

    docstring, _ = get_docstring_and_rest(filename)

    # lstrip is just in case docstring has a '\n\n' at the beginning
    paragraphs = docstring.lstrip().split('\n\n')
    if len(paragraphs) > 1:
        first_paragraph = re.sub('\n', ' ', paragraphs[1])
        first_paragraph = (first_paragraph[:95] + '...'
                           if len(first_paragraph) > 95 else first_paragraph)
    else:
        raise ValueError(
            "Example docstring should have a header for the example title "
            "and at least a paragraph explaining what the example is about. "
            "Please check the example file:\n {}\n".format(filename))

    return first_paragraph