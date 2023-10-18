def neurommsig_topology(graph: BELGraph, nodes: List[BaseEntity]) -> float:
    """Calculate the node neighbor score for a given list of nodes.
    
    -  Doesn't consider self loops

    .. math::
        
         \frac{\sum_i^n N_G[i]}{n*(n-1)}
    """
    nodes = list(nodes)
    number_nodes = len(nodes)

    if number_nodes <= 1:
        # log.debug('')
        return 0.0

    unnormalized_sum = sum(
        u in graph[v]
        for u, v in itt.product(nodes, repeat=2)
        if v in graph and u != v
    )

    return unnormalized_sum / (number_nodes * (number_nodes - 1.0))