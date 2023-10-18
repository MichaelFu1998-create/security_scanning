def bitrate(input_filepath):
    '''
    Number of bits per sample (0 if not applicable).

    Parameters
    ----------
    input_filepath : str
        Path to audio file.

    Returns
    -------
    bitrate : int
        number of bits per sample
        returns 0 if not applicable
    '''
    validate_input_file(input_filepath)
    output = soxi(input_filepath, 'b')
    if output == '0':
        logger.warning("Bitrate unavailable for %s", input_filepath)
    return int(output)