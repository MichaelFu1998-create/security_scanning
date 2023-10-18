def num_samples(input_filepath):
    '''
    Show number of samples (0 if unavailable).

    Parameters
    ----------
    input_filepath : str
        Path to audio file.

    Returns
    -------
    n_samples : int
        total number of samples in audio file.
        Returns 0 if empty or unavailable
    '''
    validate_input_file(input_filepath)
    output = soxi(input_filepath, 's')
    if output == '0':
        logger.warning("Number of samples unavailable for %s", input_filepath)
    return int(output)