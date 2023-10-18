def display_multi(annotations, fig_kw=None, meta=True, **kwargs):
    '''Display multiple annotations with shared axes

    Parameters
    ----------
    annotations : jams.AnnotationArray
        A collection of annotations to display

    fig_kw : dict
        Keyword arguments to `plt.figure`

    meta : bool
        If `True`, display annotation metadata for each annotation

    kwargs
        Additional keyword arguments to the `mir_eval.display` routines

    Returns
    -------
    fig
        The created figure
    axs
        List of subplot axes corresponding to each displayed annotation
    '''
    if fig_kw is None:
        fig_kw = dict()

    fig_kw.setdefault('sharex', True)
    fig_kw.setdefault('squeeze', True)

    # Filter down to coercable annotations first
    display_annotations = []
    for ann in annotations:
        for namespace in VIZ_MAPPING:
            if can_convert(ann, namespace):
                display_annotations.append(ann)
                break

    # If there are no displayable annotations, fail here
    if not len(display_annotations):
        raise ParameterError('No displayable annotations found')

    fig, axs = plt.subplots(nrows=len(display_annotations), ncols=1, **fig_kw)

    # MPL is stupid when making singleton subplots.
    # We catch this and make it always iterable.
    if len(display_annotations) == 1:
        axs = [axs]

    for ann, ax in zip(display_annotations, axs):
        kwargs['ax'] = ax
        display(ann, meta=meta, **kwargs)

    return fig, axs