def beat(ref, est, **kwargs):
    r'''Beat tracking evaluation

    Parameters
    ----------
    ref : jams.Annotation
        Reference annotation object
    est : jams.Annotation
        Estimated annotation object
    kwargs
        Additional keyword arguments

    Returns
    -------
    scores : dict
        Dictionary of scores, where the key is the metric name (str) and
        the value is the (float) score achieved.

    See Also
    --------
    mir_eval.beat.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='beat')[0]
    >>> est_ann = est_jam.search(namespace='beat')[0]
    >>> scores = jams.eval.beat(ref_ann, est_ann)
    '''

    namespace = 'beat'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)

    ref_times, _ = ref.to_event_values()
    est_times, _ = est.to_event_values()

    return mir_eval.beat.evaluate(ref_times, est_times, **kwargs)