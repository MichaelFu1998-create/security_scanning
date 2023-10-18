def melody(ref, est, **kwargs):
    r'''Melody extraction evaluation

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
    mir_eval.melody.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='pitch_contour')[0]
    >>> est_ann = est_jam.search(namespace='pitch_contour')[0]
    >>> scores = jams.eval.melody(ref_ann, est_ann)
    '''

    namespace = 'pitch_contour'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)

    ref_times, ref_p = ref.to_event_values()
    est_times, est_p = est.to_event_values()

    ref_freq = np.asarray([p['frequency'] * (-1)**(~p['voiced']) for p in ref_p])
    est_freq = np.asarray([p['frequency'] * (-1)**(~p['voiced']) for p in est_p])

    return mir_eval.melody.evaluate(ref_times, ref_freq,
                                    est_times, est_freq,
                                    **kwargs)