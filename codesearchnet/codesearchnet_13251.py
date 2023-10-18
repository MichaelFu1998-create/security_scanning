def beat_position(annotation, **kwargs):
    '''Plotting wrapper for beat-position data'''

    times, values = annotation.to_interval_values()

    labels = [_['position'] for _ in values]

    # TODO: plot time signature, measure number
    return mir_eval.display.events(times, labels=labels, **kwargs)