def group_errors(graph: BELGraph) -> Mapping[str, List[int]]:
    """Group the errors together for analysis of the most frequent error.

    :return: A dictionary of {error string: list of line numbers}
    """
    warning_summary = defaultdict(list)

    for _, exc, _ in graph.warnings:
        warning_summary[str(exc)].append(exc.line_number)

    return dict(warning_summary)