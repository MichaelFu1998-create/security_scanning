def slice_clip(filename, start, stop, n_samples, sr, mono=True):
    '''Slice a fragment of audio from a file.

    This uses pysoundfile to efficiently seek without
    loading the entire stream.

    Parameters
    ----------
    filename : str
        Path to the input file

    start : int
        The sample index of `filename` at which the audio fragment should start

    stop : int
        The sample index of `filename` at which the audio fragment should stop (e.g. y = audio[start:stop])

    n_samples : int > 0
        The number of samples to load

    sr : int > 0
        The target sampling rate

    mono : bool
        Ensure monophonic audio

    Returns
    -------
    y : np.ndarray [shape=(n_samples,)]
        A fragment of audio sampled from `filename`

    Raises
    ------
    ValueError
        If the source file is shorter than the requested length

    '''

    with psf.SoundFile(str(filename), mode='r') as soundf:
        n_target = stop - start

        soundf.seek(start)

        y = soundf.read(n_target).T

        if mono:
            y = librosa.to_mono(y)

        # Resample to initial sr
        y = librosa.resample(y, soundf.samplerate, sr)

        # Clip to the target length exactly
        y = librosa.util.fix_length(y, n_samples)

        return y