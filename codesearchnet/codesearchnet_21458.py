def serialize_list(out, lst, delimiter=u'', max_length=20):

    """This method is used to serialize list of text
    pieces like ["some=u'Another'", "blah=124"]

    Depending on how many lines are in these items,
    they are concatenated in row or as a column.

    Concatenation result is appended to the `out` argument.
    """

    have_multiline_items = any(map(is_multiline, lst))
    result_will_be_too_long = sum(map(len, lst)) > max_length

    if have_multiline_items or result_will_be_too_long:
        padding = len(out)
        add_padding = padding_adder(padding)

        # we need to add padding to all lines
        # except the first one
        head, rest = cut_head(lst)
        rest = map(add_padding, rest)

        # add padding to the head, but not for it's first line
        head = add_padding(head, ignore_first_line=True)

        # now join lines back
        lst = chain((head,), rest)
        delimiter += u'\n'
    else:
        delimiter += u' '

    return out + delimiter.join(lst)