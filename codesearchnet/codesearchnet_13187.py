def hierarchy_flatten(annotation):
    '''Flatten a multi_segment annotation into mir_eval style.

    Parameters
    ----------
    annotation : jams.Annotation
        An annotation in the `multi_segment` namespace

    Returns
    -------
    hier_intervalss : list
        A list of lists of intervals, ordered by increasing specificity.

    hier_labels : list
        A list of lists of labels, ordered by increasing specificity.
    '''

    intervals, values = annotation.to_interval_values()

    ordering = dict()

    for interval, value in zip(intervals, values):
        level = value['level']
        if level not in ordering:
            ordering[level] = dict(intervals=list(), labels=list())

        ordering[level]['intervals'].append(interval)
        ordering[level]['labels'].append(value['label'])

    levels = sorted(list(ordering.keys()))
    hier_intervals = [ordering[level]['intervals'] for level in levels]
    hier_labels = [ordering[level]['labels'] for level in levels]

    return hier_intervals, hier_labels