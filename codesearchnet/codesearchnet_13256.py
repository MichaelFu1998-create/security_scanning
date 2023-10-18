def clicks(annotation, sr=22050, length=None, **kwargs):
    '''Sonify events with clicks.

    This uses mir_eval.sonify.clicks, and is appropriate for instantaneous
    events such as beats or segment boundaries.
    '''

    interval, _ = annotation.to_interval_values()

    return filter_kwargs(mir_eval.sonify.clicks, interval[:, 0],
                         fs=sr, length=length, **kwargs)