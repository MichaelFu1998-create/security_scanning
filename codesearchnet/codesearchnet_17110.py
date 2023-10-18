def main(output):
    """Output the HBP knowledge graph to the desktop"""
    from hbp_knowledge import get_graph
    graph = get_graph()
    text = to_html(graph)
    print(text, file=output)