def chord(ref, est, **kwargs):
    r'''Chord evaluation

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
    mir_eval.chord.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='chord')[0]
    >>> est_ann = est_jam.search(namespace='chord')[0]
    >>> scores = jams.eval.chord(ref_ann, est_ann)
    '''

    namespace = 'chord'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)
    ref_interval, ref_value = ref.to_interval_values()
    est_interval, est_value = est.to_interval_values()

    return mir_eval.chord.evaluate(ref_interval, ref_value,
                                   est_interval, est_value, **kwargs)