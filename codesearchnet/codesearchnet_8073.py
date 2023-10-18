def sample_clip_indices(filename, n_samples, sr):
    '''Calculate the indices at which to sample a fragment of audio from a file.

    Parameters
    ----------
    filename : str
        Path to the input file

    n_samples : int > 0
        The number of samples to load

    sr : int > 0
        The target sampling rate

    Returns
    -------
    start : int
        The sample index from `filename` at which the audio fragment starts
    stop : int
        The sample index from `filename` at which the audio fragment stops (e.g. y = audio[start:stop])
    '''

    with psf.SoundFile(str(filename), mode='r') as soundf:
        # Measure required length of fragment
        n_target = int(np.ceil(n_samples * soundf.samplerate / float(sr)))

        # Raise exception if source is too short
        if len(soundf) < n_target:
            raise RuntimeError('Source {} (length={})'.format(filename, len(soundf)) +
                ' must be at least the length of the input ({})'.format(n_target))

        # Draw a starting point at random in the background waveform
        start = np.random.randint(0, 1 + len(soundf) - n_target)
        stop = start + n_target

        return start, stop