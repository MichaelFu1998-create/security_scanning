def update_context(universe: BELGraph, graph: BELGraph):
    """Update the context of a subgraph from the universe of all knowledge."""
    for namespace in get_namespaces(graph):
        if namespace in universe.namespace_url:
            graph.namespace_url[namespace] = universe.namespace_url[namespace]
        elif namespace in universe.namespace_pattern:
            graph.namespace_pattern[namespace] = universe.namespace_pattern[namespace]
        else:
            log.warning('namespace: %s missing from universe', namespace)

    for annotation in get_annotations(graph):
        if annotation in universe.annotation_url:
            graph.annotation_url[annotation] = universe.annotation_url[annotation]
        elif annotation in universe.annotation_pattern:
            graph.annotation_pattern[annotation] = universe.annotation_pattern[annotation]
        elif annotation in universe.annotation_list:
            graph.annotation_list[annotation] = universe.annotation_list[annotation]
        else:
            log.warning('annotation: %s missing from universe', annotation)