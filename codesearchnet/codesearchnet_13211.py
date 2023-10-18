def convert(annotation, target_namespace):
    '''Convert a given annotation to the target namespace.

    Parameters
    ----------
    annotation : jams.Annotation
        An annotation object

    target_namespace : str
        The target namespace

    Returns
    -------
    mapped_annotation : jams.Annotation
        if `annotation` already belongs to `target_namespace`, then
        it is returned directly.

        otherwise, `annotation` is copied and automatically converted
        to the target namespace.

    Raises
    ------
    SchemaError
        if the input annotation fails to validate

    NamespaceError
        if no conversion is possible

    Examples
    --------
    Convert frequency measurements in Hz to MIDI

    >>> ann_midi = jams.convert(ann_hz, 'note_midi')

    And back to Hz

    >>> ann_hz2 = jams.convert(ann_midi, 'note_hz')
    '''

    # First, validate the input. If this fails, we can't auto-convert.
    annotation.validate(strict=True)

    # If we're already in the target namespace, do nothing
    if annotation.namespace == target_namespace:
        return annotation

    if target_namespace in __CONVERSION__:
        # Otherwise, make a copy to mangle
        annotation = deepcopy(annotation)

        # Look for a way to map this namespace to the target
        for source in __CONVERSION__[target_namespace]:
            if annotation.search(namespace=source):
                return __CONVERSION__[target_namespace][source](annotation)

    # No conversion possible
    raise NamespaceError('Unable to convert annotation from namespace='
                         '"{0}" to "{1}"'.format(annotation.namespace,
                                                 target_namespace))