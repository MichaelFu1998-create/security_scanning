def scaled_fft(fft, scale=1.0):
    """
    Produces a nicer graph, I'm not sure if this is correct
    """
    data = np.zeros(len(fft))
    for i, v in enumerate(fft):
        data[i] = scale * (i * v) / NUM_SAMPLES

    return data