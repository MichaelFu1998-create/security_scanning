def count_citation_years(graph: BELGraph) -> typing.Counter[int]:
    """Count the number of citations from each year."""
    result = defaultdict(set)

    for _, _, data in graph.edges(data=True):
        if CITATION not in data or CITATION_DATE not in data[CITATION]:
            continue

        try:
            dt = _ensure_datetime(data[CITATION][CITATION_DATE])
            result[dt.year].add((data[CITATION][CITATION_TYPE], data[CITATION][CITATION_REFERENCE]))
        except Exception:
            continue

    return count_dict_values(result)