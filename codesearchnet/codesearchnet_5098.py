def render_ranks (graph, ranks, dot_file="graph.dot"):
    """
    render the TextRank graph for visual formats
    """
    if dot_file:
        write_dot(graph, ranks, path=dot_file)