def collapse_nodes_with_same_names(graph: BELGraph) -> None:
    """Collapse all nodes with the same name, merging namespaces by picking first alphabetical one."""
    survivor_mapping = defaultdict(set) # Collapse mapping dict
    victims = set() # Things already mapped while iterating

    it = tqdm(itt.combinations(graph, r=2), total=graph.number_of_nodes() * (graph.number_of_nodes() - 1) / 2)
    for a, b in it:
        if b in victims:
            continue

        a_name, b_name = a.get(NAME), b.get(NAME)
        if not a_name or not b_name or a_name.lower() != b_name.lower():
            continue

        if a.keys() != b.keys():  # not same version (might have variants)
            continue

        # Ensure that the values in the keys are also the same
        for k in set(a.keys()) - {NAME, NAMESPACE}:
            if a[k] != b[k]:  # something different
                continue

        survivor_mapping[a].add(b)
        # Keep track of things that has been already mapped
        victims.add(b)

    collapse_nodes(graph, survivor_mapping)