def pattern(ref, est, **kwargs):
    r'''Pattern detection evaluation

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
    mir_eval.pattern.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='pattern_jku')[0]
    >>> est_ann = est_jam.search(namespace='pattern_jku')[0]
    >>> scores = jams.eval.pattern(ref_ann, est_ann)
    '''

    namespace = 'pattern_jku'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)

    ref_patterns = pattern_to_mireval(ref)
    est_patterns = pattern_to_mireval(est)

    return mir_eval.pattern.evaluate(ref_patterns, est_patterns, **kwargs)