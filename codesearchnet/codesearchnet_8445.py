def emph(txt, rval=None):
    """Print, emphasized based on rval"""

    if rval is None:    # rval is not specified, use 'neutral'
        info(txt)
    elif rval == 0:     # rval is 0, by convention, this is 'good'
        good(txt)
    else:               # any other value, considered 'bad'
        err(txt)