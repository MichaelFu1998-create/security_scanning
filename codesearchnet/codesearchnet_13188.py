def hierarchy(ref, est, **kwargs):
    r'''Multi-level segmentation evaluation

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
    mir_eval.hierarchy.evaluate

    Examples
    --------
    >>> # Load in the JAMS objects
    >>> ref_jam = jams.load('reference.jams')
    >>> est_jam = jams.load('estimated.jams')
    >>> # Select the first relevant annotations
    >>> ref_ann = ref_jam.search(namespace='multi_segment')[0]
    >>> est_ann = est_jam.search(namespace='multi_segment')[0]
    >>> scores = jams.eval.hierarchy(ref_ann, est_ann)
    '''
    namespace = 'multi_segment'
    ref = coerce_annotation(ref, namespace)
    est = coerce_annotation(est, namespace)
    ref_hier, ref_hier_lab = hierarchy_flatten(ref)
    est_hier, est_hier_lab = hierarchy_flatten(est)

    return mir_eval.hierarchy.evaluate(ref_hier, ref_hier_lab,
                                       est_hier, est_hier_lab,
                                       **kwargs)