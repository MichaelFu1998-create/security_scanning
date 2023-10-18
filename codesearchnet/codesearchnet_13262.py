def sonify(annotation, sr=22050, duration=None, **kwargs):
    '''Sonify a jams annotation through mir_eval

    Parameters
    ----------
    annotation : jams.Annotation
        The annotation to sonify

    sr = : positive number
        The sampling rate of the output waveform

    duration : float (optional)
        Optional length (in seconds) of the output waveform

    kwargs
        Additional keyword arguments to mir_eval.sonify functions

    Returns
    -------
    y_sonified : np.ndarray
        The waveform of the sonified annotation

    Raises
    ------
    NamespaceError
        If the annotation has an un-sonifiable namespace
    '''

    length = None

    if duration is None:
        duration = annotation.duration

    if duration is not None:
        length = int(duration * sr)

    # If the annotation can be directly sonified, try that first
    if annotation.namespace in SONIFY_MAPPING:
        ann = coerce_annotation(annotation, annotation.namespace)
        return SONIFY_MAPPING[annotation.namespace](ann,
                                                    sr=sr,
                                                    length=length,
                                                    **kwargs)

    for namespace, func in six.iteritems(SONIFY_MAPPING):
        try:
            ann = coerce_annotation(annotation, namespace)
            return func(ann, sr=sr, length=length, **kwargs)
        except NamespaceError:
            pass

    raise NamespaceError('Unable to sonify annotation of namespace="{:s}"'
                         .format(annotation.namespace))