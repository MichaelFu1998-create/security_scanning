def silent(input_filepath, threshold=0.001):
    '''
    Determine if an input file is silent.

    Parameters
    ----------
    input_filepath : str
        The input filepath.
    threshold : float
        Threshold for determining silence

    Returns
    -------
    is_silent : bool
        True if file is determined silent.
    '''
    validate_input_file(input_filepath)
    stat_dictionary = stat(input_filepath)
    mean_norm = stat_dictionary['Mean    norm']
    if mean_norm is not float('nan'):
        if mean_norm >= threshold:
            return False
        else:
            return True
    else:
        return True