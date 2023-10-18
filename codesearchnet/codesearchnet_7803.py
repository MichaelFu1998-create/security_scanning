def _get_valid_formats():
    ''' Calls SoX help for a lists of audio formats available with the current
    install of SoX.

    Returns:
    --------
    formats : list
        List of audio file extensions that SoX can process.

    '''
    if NO_SOX:
        return []

    so = subprocess.check_output(['sox', '-h'])
    if type(so) is not str:
        so = str(so, encoding='UTF-8')
    so = so.split('\n')
    idx = [i for i in range(len(so)) if 'AUDIO FILE FORMATS:' in so[i]][0]
    formats = so[idx].split(' ')[3:]

    return formats