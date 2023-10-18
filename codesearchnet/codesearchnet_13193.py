def transcription(ref, est, **kwargs):
    r'''Note transcription evaluation

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
    mir_eval.transcription.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations. You can use any annotation
    >>> # type that can be converted to pitch_contour (such as pitch_midi)
    >>> ref_ann = ref_jam.search(namespace='pitch_contour')[0]
    >>> est_ann = est_jam.search(namespace='note_hz')[0]
    >>> scores = jams.eval.transcription(ref_ann, est_ann)
    '''

    namespace = 'pitch_contour'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)
    ref_intervals, ref_p = ref.to_interval_values()
    est_intervals, est_p = est.to_interval_values()

    ref_pitches = np.asarray([p['frequency'] * (-1)**(~p['voiced']) for p in ref_p])
    est_pitches = np.asarray([p['frequency'] * (-1)**(~p['voiced']) for p in est_p])

    return mir_eval.transcription.evaluate(
        ref_intervals, ref_pitches, est_intervals, est_pitches, **kwargs)