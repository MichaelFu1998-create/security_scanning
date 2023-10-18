def body(quantity=2, separator='\n\n', wrap_start='', wrap_end='',
         html=False, sentences_quantity=3, as_list=False):
    """Return a random email text."""
    return lorem_ipsum.paragraphs(quantity=quantity, separator=separator,
                                  wrap_start=wrap_start, wrap_end=wrap_end,
                                  html=html,
                                  sentences_quantity=sentences_quantity,
                                  as_list=as_list)