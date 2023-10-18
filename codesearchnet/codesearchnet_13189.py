def tempo(ref, est, **kwargs):
    r'''Tempo evaluation

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
    mir_eval.tempo.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='tempo')[0]
    >>> est_ann = est_jam.search(namespace='tempo')[0]
    >>> scores = jams.eval.tempo(ref_ann, est_ann)
    '''

    ref = coerce_annotation(ref, 'tempo')
    est = coerce_annotation(est, 'tempo')

    ref_tempi = np.asarray([o.value for o in ref])
    ref_weight = ref.data[0].confidence
    est_tempi = np.asarray([o.value for o in est])

    return mir_eval.tempo.evaluate(ref_tempi, ref_weight, est_tempi, **kwargs)