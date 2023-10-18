def coerce_annotation(ann, namespace):
    '''Validate that the annotation has the correct namespace,
    and is well-formed.

    If the annotation is not of the correct namespace, automatic conversion
    is attempted.

    Parameters
    ----------
    ann : jams.Annotation
        The annotation object in question

    namespace : str
        The namespace pattern to match `ann` against

    Returns
    -------
    ann_coerced: jams.Annotation
        The annotation coerced to the target namespace

    Raises
    ------
    NamespaceError
        If `ann` does not match the proper namespace

    SchemaError
        If `ann` fails schema validation

    See Also
    --------
    jams.nsconvert.convert
    '''

    ann = convert(ann, namespace)
    ann.validate(strict=True)

    return ann