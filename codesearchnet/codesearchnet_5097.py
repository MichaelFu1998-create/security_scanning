def write_dot (graph, ranks, path="graph.dot"):
    """
    output the graph in Dot file format
    """
    dot = Digraph()

    for node in graph.nodes():
        dot.node(node, "%s %0.3f" % (node, ranks[node]))

    for edge in graph.edges():
        dot.edge(edge[0], edge[1], constraint="false")

    with open(path, 'w') as f:
        f.write(dot.source)