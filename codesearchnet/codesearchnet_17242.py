def build_edge_data_filter(annotations: Mapping, partial_match: bool = True) -> EdgePredicate: # noqa: D202
    """Build a filter that keeps edges whose data dictionaries are super-dictionaries to the given dictionary.

    :param annotations: The annotation query dict to match
    :param partial_match: Should the query values be used as partial or exact matches? Defaults to :code:`True`.
    """

    @edge_predicate
    def annotation_dict_filter(data: EdgeData) -> bool:
        """A filter that matches edges with the given dictionary as a sub-dictionary."""
        return subdict_matches(data, annotations, partial_match=partial_match)

    return annotation_dict_filter