def flatten_fft(scale=1.0):
    """
    Produces a nicer graph, I'm not sure if this is correct
    """
    _len = len(audio.spectrogram)
    for i, v in enumerate(audio.spectrogram):
        yield scale * (i * v) / _len