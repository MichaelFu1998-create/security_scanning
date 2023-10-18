def intervals(annotation, **kwargs):
    '''Plotting wrapper for labeled intervals'''
    times, labels = annotation.to_interval_values()

    return mir_eval.display.labeled_intervals(times, labels, **kwargs)