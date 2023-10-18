def event(annotation, **kwargs):
    '''Plotting wrapper for events'''

    times, values = annotation.to_interval_values()

    if any(values):
        labels = values
    else:
        labels = None

    return mir_eval.display.events(times, labels=labels, **kwargs)