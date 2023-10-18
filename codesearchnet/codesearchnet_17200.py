def bel_to_spia_matrices(graph: BELGraph) -> Mapping[str, pd.DataFrame]:
    """Create an excel sheet ready to be used in SPIA software.

    :param graph: BELGraph
    :return: dictionary with matrices
    """
    index_nodes = get_matrix_index(graph)
    spia_matrices = build_spia_matrices(index_nodes)

    for u, v, edge_data in graph.edges(data=True):
        # Both nodes are CentralDogma abundances
        if isinstance(u, CentralDogma) and isinstance(v, CentralDogma):
            # Update matrix dict
            update_spia_matrices(spia_matrices, u, v, edge_data)

        # Subject is CentralDogmaAbundance and node is ListAbundance
        elif isinstance(u, CentralDogma) and isinstance(v, ListAbundance):
            # Add a relationship from subject to each of the members in the object
            for node in v.members:
                # Skip if the member is not in CentralDogma
                if not isinstance(node, CentralDogma):
                    continue

                update_spia_matrices(spia_matrices, u, node, edge_data)

        # Subject is ListAbundance and node is CentralDogmaAbundance
        elif isinstance(u, ListAbundance) and isinstance(v, CentralDogma):
            # Add a relationship from each of the members of the subject to the object
            for node in u.members:
                # Skip if the member is not in CentralDogma
                if not isinstance(node, CentralDogma):
                    continue

                update_spia_matrices(spia_matrices, node, v, edge_data)

        # Both nodes are ListAbundance
        elif isinstance(u, ListAbundance) and isinstance(v, ListAbundance):
            for sub_member, obj_member in product(u.members, v.members):
                # Update matrix if both are CentralDogma
                if isinstance(sub_member, CentralDogma) and isinstance(obj_member, CentralDogma):
                    update_spia_matrices(spia_matrices, sub_member, obj_member, edge_data)

        # else Not valid edge

    return spia_matrices