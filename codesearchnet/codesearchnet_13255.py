def mkclick(freq, sr=22050, duration=0.1):
    '''Generate a click sample.

    This replicates functionality from mir_eval.sonify.clicks,
    but exposes the target frequency and duration.
    '''

    times = np.arange(int(sr * duration))
    click = np.sin(2 * np.pi * times * freq / float(sr))
    click *= np.exp(- times / (1e-2 * sr))

    return click