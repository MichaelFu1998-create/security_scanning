def duration(input_filepath):
    '''
    Show duration in seconds (0 if unavailable).

    Parameters
    ----------
    input_filepath : str
        Path to audio file.

    Returns
    -------
    duration : float
        Duration of audio file in seconds.
        If unavailable or empty, returns 0.
    '''
    validate_input_file(input_filepath)
    output = soxi(input_filepath, 'D')
    if output == '0':
        logger.warning("Duration unavailable for %s", input_filepath)

    return float(output)