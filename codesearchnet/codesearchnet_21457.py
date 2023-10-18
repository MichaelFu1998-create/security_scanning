def serialize_text(out, text):
    """This method is used to append content of the `text`
    argument to the `out` argument.

    Depending on how many lines in the text, a
    padding can be added to all lines except the first
    one.

    Concatenation result is appended to the `out` argument.
    """
    padding = len(out)
    # we need to add padding to all lines
    # except the first one
    add_padding = padding_adder(padding)
    text = add_padding(text, ignore_first_line=True)

    return out + text