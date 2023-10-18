def match_simple_metapath(graph, node, simple_metapath):
    """Matches a simple metapath starting at the given node

    :param pybel.BELGraph graph: A BEL graph
    :param tuple node: A BEL node
    :param list[str] simple_metapath: A list of BEL Functions
    :return: An iterable over paths from the node matching the metapath
    :rtype: iter[tuple]
    """
    if 0 == len(simple_metapath):
        yield node,

    else:
        for neighbor in graph.edges[node]:
            if graph.nodes[neighbor][FUNCTION] == simple_metapath[0]:
                for path in match_simple_metapath(graph, neighbor, simple_metapath[1:]):
                    if node not in path:
                        yield (node,) + path