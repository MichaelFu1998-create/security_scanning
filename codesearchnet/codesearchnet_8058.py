def load_jam_audio(jam_in, audio_file,
                   validate=True,
                   strict=True,
                   fmt='auto',
                   **kwargs):
    '''Load a jam and pack it with audio.

    Parameters
    ----------
    jam_in : str, file descriptor, or jams.JAMS
        JAMS filename, open file-descriptor, or object to load.
        See ``jams.load`` for acceptable formats.

    audio_file : str
        Audio filename to load

    validate : bool
    strict : bool
    fmt : str
        Parameters to `jams.load`

    kwargs : additional keyword arguments
        See `librosa.load`

    Returns
    -------
    jam : jams.JAMS
        A jams object with audio data in the top-level sandbox

    Notes
    -----
    This operation can modify the `file_metadata.duration` field of `jam_in`:
    If it is not currently set, it will be populated with the duration of the
    audio file.

    See Also
    --------
    jams.load
    librosa.core.load
    '''

    if isinstance(jam_in, jams.JAMS):
        jam = jam_in
    else:
        jam = jams.load(jam_in, validate=validate, strict=strict, fmt=fmt)

    y, sr = librosa.load(audio_file, **kwargs)

    if jam.file_metadata.duration is None:
        jam.file_metadata.duration = librosa.get_duration(y=y, sr=sr)

    return jam_pack(jam, _audio=dict(y=y, sr=sr))