def punctuate_authorname(an):
    """Punctuate author names properly.

    Expects input in the form 'Bloggs, J K' and will return 'Bloggs, J. K.'.
    """
    name = an.strip()
    parts = [x for x in name.split(',') if x != '']
    ret_str = ''
    for idx, part in enumerate(parts):
        subparts = part.strip().split(' ')
        for sidx, substr in enumerate(subparts):
            ret_str += substr
            if len(substr) == 1:
                ret_str += '.'
            if sidx < (len(subparts) - 1):
                ret_str += ' '
        if idx < (len(parts) - 1):
            ret_str += ', '
    return ret_str.strip()