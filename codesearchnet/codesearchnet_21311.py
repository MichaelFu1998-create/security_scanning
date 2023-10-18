def f_annotation_filter(annotations, type_uri, number):
    """ Annotation filtering filter

    :param annotations: List of annotations
    :type annotations: [AnnotationResource]
    :param type_uri: URI Type on which to filter
    :type type_uri: str
    :param number: Number of the annotation to return
    :type number: int
    :return: Annotation(s) matching the request
    :rtype: [AnnotationResource] or AnnotationResource
    """
    filtered = [
        annotation
        for annotation in annotations
        if annotation.type_uri == type_uri
    ]
    number = min([len(filtered), number])
    if number == 0:
        return None
    else:
        return filtered[number-1]