def write_dot_file(G, filename):
    """
    Writes the graph G in dot file format for graphviz visualization.

    Args:
        a Networkx graph
        A filename to name the dot files
    """
    with io.open(filename, "w") as fh:
        fh.write("strict digraph DependencyDiagram {\n")
        edge_list = G.edges()
        node_list = set(G.nodes())
        if edge_list:
            for edge in sorted(edge_list):
                source, targ = edge
                node_list = node_list - set(source)
                node_list = node_list - set(targ)
                line = '"{}" -> "{}";\n'
                fh.write(line.format(source, targ))
        # draw nodes with no links
        if node_list:
            for node in sorted(node_list):
                line = '"{}"\n'.format(node)
                fh.write(line)
        fh.write("}")