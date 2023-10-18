def to_jupyter(graph: BELGraph, chart: Optional[str] = None) -> Javascript:
    """Render the graph as JavaScript in a Jupyter Notebook."""
    with open(os.path.join(HERE, 'render_with_javascript.js'), 'rt') as f:
        js_template = Template(f.read())

    return Javascript(js_template.render(**_get_context(graph, chart=chart)))