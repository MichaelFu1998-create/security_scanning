def build_graph (json_iter):
    """
    construct the TextRank graph from parsed paragraphs
    """
    global DEBUG, WordNode
    graph = nx.DiGraph()

    for meta in json_iter:
        if DEBUG:
            print(meta["graf"])

        for pair in get_tiles(map(WordNode._make, meta["graf"])):
            if DEBUG:
                print(pair)

            for word_id in pair:
                if not graph.has_node(word_id):
                    graph.add_node(word_id)

            try:
                graph.edge[pair[0]][pair[1]]["weight"] += 1.0
            except KeyError:
                graph.add_edge(pair[0], pair[1], weight=1.0)

    return graph