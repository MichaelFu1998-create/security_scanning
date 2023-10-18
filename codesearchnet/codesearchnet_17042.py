def to_html(graph: BELGraph, chart: Optional[str] = None) -> str:
    """Render the graph as an HTML string.

    Common usage may involve writing to a file like:

    >>> from pybel.examples import sialic_acid_graph
    >>> with open('ideogram_output.html', 'w') as file:
    ...     print(to_html(sialic_acid_graph), file=file)
    """
    with open(os.path.join(HERE, 'index.html'), 'rt') as f:
        html_template = Template(f.read())

    return html_template.render(**_get_context(graph, chart=chart))