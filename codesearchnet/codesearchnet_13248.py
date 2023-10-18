def hierarchy(annotation, **kwargs):
    '''Plotting wrapper for hierarchical segmentations'''
    htimes, hlabels = hierarchy_flatten(annotation)

    htimes = [np.asarray(_) for _ in htimes]
    return mir_eval.display.hierarchy(htimes, hlabels, **kwargs)