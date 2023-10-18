def save(filename_audio, filename_jam, jam, strict=True, fmt='auto', **kwargs):
    '''Save a muda jam to disk

    Parameters
    ----------
    filename_audio: str
        The path to store the audio file

    filename_jam: str
        The path to store the jams object

    strict: bool
        Strict safety checking for jams output

    fmt : str
        Output format parameter for `jams.JAMS.save`

    kwargs
        Additional parameters to `soundfile.write`
    '''

    y = jam.sandbox.muda._audio['y']
    sr = jam.sandbox.muda._audio['sr']

    # First, dump the audio file
    psf.write(filename_audio, y, sr, **kwargs)

    # Then dump the jam
    jam.save(filename_jam, strict=strict, fmt=fmt)