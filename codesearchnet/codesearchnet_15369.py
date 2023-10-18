def graph(networkx_graph, title='Axial Graph Visualization', scripts_mode="CDN", data_mode="directory",
          output_dir=".", filename="graph.html", version=this_version):
    """
    Arguments:
        networkx_graph (networkx.Graph): any instance of networkx.Graph
        title (str): The title of the plot (to be embedded in the html).
        scripts_mode (str): Choose from [`"CDN"`, `"directory"`, `"inline"`]:

            - `"CDN"` compiles a single HTML page with links to scripts hosted on a CDN,

            - `"directory"` compiles a directory with all scripts locally cached,

            - `"inline"` compiles a single HTML file with all scripts/styles inlined.

        data_mode (str): Choose from ["directory", "inline"]:

            - "directory" compiles a directory with all data locally cached,

            - "inline" compiles a single HTML file with all data inlined.

        output_dir (str): the directory in which to output the file
        filename (str): the filename of the output file
        version (str): the version of the javascripts to use.
            Leave the default to pin the version, or choose "latest" to get updates,
            or choose part of the version string to get minor updates.
    Returns:
        Path: The filepath which the html was outputted to.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Scripts =======================

    scripts = third_party_scripts + [CDN_url(version)+"js/cola.min.js", CDN_url(version)+"js/graph.js"]

    scripts_block = _scripts_block(scripts, scripts_mode, output_dir)

    # Data    =======================

    graph_json = nx_json.node_link_data(networkx_graph)

    for node in graph_json['nodes']:
        for attr, val in node.items():
            if isinstance(val, numbers.Number):
                node[attr] = round(val, 2)
    for link in graph_json['links']:
        for attr, val in link.items():
            if isinstance(val, numbers.Number):
                link[attr] = round(val, 2)

    graph_json = f"var graph = {json.dumps(graph_json)};"

    data_block = _data_block(data_mode, [('graph', graph_json)], output_dir)

    html = templateEnv.get_template('graph.html.j2').render(title=title, scripts_block=scripts_block+'\n'+data_block, nodes=networkx_graph.nodes())

    (output_dir / filename).write_text(html)

    return (output_dir / filename).resolve()