def _stat_call(filepath):
    '''Call sox's stat function.

    Parameters
    ----------
    filepath : str
        File path.

    Returns
    -------
    stat_output : str
        Sox output from stderr.
    '''
    validate_input_file(filepath)
    args = ['sox', filepath, '-n', 'stat']
    _, _, stat_output = sox(args)
    return stat_output