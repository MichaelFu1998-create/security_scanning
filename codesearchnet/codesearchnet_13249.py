def pitch_contour(annotation, **kwargs):
    '''Plotting wrapper for pitch contours'''
    ax = kwargs.pop('ax', None)

    # If the annotation is empty, we need to construct a new axes
    ax = mir_eval.display.__get_axes(ax=ax)[0]

    times, values = annotation.to_interval_values()

    indices = np.unique([v['index'] for v in values])

    for idx in indices:
        rows = [i for (i, v) in enumerate(values) if v['index'] == idx]
        freqs = np.asarray([values[r]['frequency'] for r in rows])
        unvoiced = ~np.asarray([values[r]['voiced'] for r in rows])
        freqs[unvoiced] *= -1

        ax = mir_eval.display.pitch(times[rows, 0], freqs, unvoiced=True,
                                    ax=ax,
                                    **kwargs)
    return ax