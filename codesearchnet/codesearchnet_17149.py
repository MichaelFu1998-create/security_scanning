def calculate_incorrect_name_dict(graph: BELGraph) -> Mapping[str, str]:
    """Group all of the incorrect identifiers in a dict of {namespace: list of erroneous names}.

    :return: A dictionary of {namespace: list of erroneous names}
    """
    missing = defaultdict(list)

    for _, e, ctx in graph.warnings:
        if not isinstance(e, (MissingNamespaceNameWarning, MissingNamespaceRegexWarning)):
            continue
        missing[e.namespace].append(e.name)

    return dict(missing)