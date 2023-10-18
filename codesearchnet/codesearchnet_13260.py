def pitch_contour(annotation, sr=22050, length=None, **kwargs):
    '''Sonify pitch contours.

    This uses mir_eval.sonify.pitch_contour, and should only be applied
    to pitch annotations using the pitch_contour namespace.

    Each contour is sonified independently, and the resulting waveforms
    are summed together.
    '''

    # Map contours to lists of observations

    times = defaultdict(list)
    freqs = defaultdict(list)

    for obs in annotation:
        times[obs.value['index']].append(obs.time)
        freqs[obs.value['index']].append(obs.value['frequency'] *
                                         (-1)**(~obs.value['voiced']))

    y_out = 0.0
    for ix in times:
        y_out = y_out + filter_kwargs(mir_eval.sonify.pitch_contour,
                                      np.asarray(times[ix]),
                                      np.asarray(freqs[ix]),
                                      fs=sr, length=length,
                                      **kwargs)
        if length is None:
            length = len(y_out)

    return y_out