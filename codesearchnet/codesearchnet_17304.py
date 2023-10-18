def get_annotations_containing_keyword(graph: BELGraph, keyword: str) -> List[Mapping[str, str]]:
    """Get annotation/value pairs for values for whom the search string is a substring

    :param graph: A BEL graph
    :param keyword: Search for annotations whose values have this as a substring
    """
    return [
        {
            'annotation': annotation,
            'value': value
        }
        for annotation, value in iter_annotation_value_pairs(graph)
        if keyword.lower() in value.lower()
    ]