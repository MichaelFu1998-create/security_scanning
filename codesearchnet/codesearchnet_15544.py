def split_unit(value):
    """ Split a number from its unit
        1px -> (q, 'px')
    Args:
        value (str): input
    returns:
        tuple
    """
    r = re.search('^(\-?[\d\.]+)(.*)$', str(value))
    return r.groups() if r else ('', '')