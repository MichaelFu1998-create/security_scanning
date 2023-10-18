def paragraphs(quantity=2, separator='\n\n', wrap_start='', wrap_end='',
               html=False, sentences_quantity=3, as_list=False):
    """Return random paragraphs."""
    if html:
        wrap_start = '<p>'
        wrap_end = '</p>'
        separator = '\n\n'

    result = []
    try:
        for _ in xrange(0, quantity):
            result.append(wrap_start +
                          sentences(sentences_quantity) +
                          wrap_end)
    # Python 3 compatibility
    except NameError:
        for _ in range(0, quantity):
            result.append(wrap_start +
                          sentences(sentences_quantity) +
                          wrap_end)

    if as_list:
        return result
    else:
        return separator.join(result)