def info(filepath):
    '''Get a dictionary of file information

    Parameters
    ----------
    filepath : str
        File path.

    Returns:
    --------
    info_dictionary : dict
        Dictionary of file information. Fields are:
            * channels
            * sample_rate
            * bitrate
            * duration
            * num_samples
            * encoding
            * silent
    '''
    info_dictionary = {
        'channels': channels(filepath),
        'sample_rate': sample_rate(filepath),
        'bitrate': bitrate(filepath),
        'duration': duration(filepath),
        'num_samples': num_samples(filepath),
        'encoding': encoding(filepath),
        'silent': silent(filepath)
    }
    return info_dictionary