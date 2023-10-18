def text(what="sentence", *args, **kwargs):
    """An aggregator for all above defined public methods."""

    if what == "character":
        return character(*args, **kwargs)
    elif what == "characters":
        return characters(*args, **kwargs)
    elif what == "word":
        return word(*args, **kwargs)
    elif what == "words":
        return words(*args, **kwargs)
    elif what == "sentence":
        return sentence(*args, **kwargs)
    elif what == "sentences":
        return sentences(*args, **kwargs)
    elif what == "paragraph":
        return paragraph(*args, **kwargs)
    elif what == "paragraphs":
        return paragraphs(*args, **kwargs)
    elif what == "title":
        return title(*args, **kwargs)
    else:
        raise NameError('No such method')