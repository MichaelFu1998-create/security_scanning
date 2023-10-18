def _parse_stat(stat_output):
    '''Parse the string output from sox's stat function

    Parameters
    ----------
    stat_output : str
        Sox output from stderr.

    Returns
    -------
    stat_dictionary : dict
        Dictionary of audio statistics.
    '''
    lines = stat_output.split('\n')
    stat_dict = {}
    for line in lines:
        split_line = line.split(':')
        if len(split_line) == 2:
            key = split_line[0]
            val = split_line[1].strip(' ')
            try:
                val = float(val)
            except ValueError:
                val = None
            stat_dict[key] = val

    return stat_dict