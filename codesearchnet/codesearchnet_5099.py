def text_rank (path):
    """
    run the TextRank algorithm
    """
    graph = build_graph(json_iter(path))
    ranks = nx.pagerank(graph)

    return graph, ranks