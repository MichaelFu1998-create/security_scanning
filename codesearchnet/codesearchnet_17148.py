def get_undefined_annotations(graph: BELGraph) -> Set[str]:
    """Get all annotations that aren't actually defined.
    
    :return: The set of all undefined annotations
    """
    return {
        exc.annotation
        for _, exc, _ in graph.warnings
        if isinstance(exc, UndefinedAnnotationWarning)
    }