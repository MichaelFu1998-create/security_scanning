def find_activations(graph: BELGraph):
    """Find edges that are A - A, meaning that some conditions in the edge best describe the interaction."""
    for u, v, key, data in graph.edges(keys=True, data=True):
        if u != v:
            continue

        bel = graph.edge_to_bel(u, v, data)

        line = data.get(LINE)

        if line is None:
            continue  # this was inferred, so need to investigate another way

        elif has_protein_modification_increases_activity(graph, u, v, key):
            print(line, '- pmod changes -', bel)
            find_related(graph, v, data)

        elif has_degradation_increases_activity(data):
            print(line, '- degradation changes -', bel)
            find_related(graph, v, data)

        elif has_translocation_increases_activity(data):
            print(line, '- translocation changes -', bel)
            find_related(graph, v, data)

        elif complex_increases_activity(graph, u, v, key):
            print(line, '- complex changes - ', bel)
            find_related(graph, v, data)

        elif has_same_subject_object(graph, u, v, key):
            print(line, '- same sub/obj -', bel)

        else:
            print(line, '- *** - ', bel)