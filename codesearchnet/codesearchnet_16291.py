def construct_graph(sakefile, settings):
    """
    Takes the sakefile dictionary and builds a NetworkX graph

    Args:
        A dictionary that is the parsed Sakefile (from sake.py)
        The settings dictionary

    Returns:
        A NetworkX graph
    """
    verbose = settings["verbose"]
    sprint = settings["sprint"]
    G = nx.DiGraph()
    sprint("Going to construct Graph", level="verbose")
    for target in sakefile:
        if target == "all":
            # we don't want this node
            continue
        if "formula" not in sakefile[target]:
            # that means this is a meta target
            for atomtarget in sakefile[target]:
                if atomtarget == "help":
                    continue
                sprint("Adding '{}'".format(atomtarget), level="verbose")
                data_dict = sakefile[target][atomtarget]
                data_dict["parent"] = target
                G.add_node(atomtarget, **data_dict)
        else:
            sprint("Adding '{}'".format(target), level="verbose")
            G.add_node(target, **sakefile[target])
    sprint("Nodes are built\nBuilding connections", level="verbose")
    for node in G.nodes(data=True):
        sprint("checking node {} for dependencies".format(node[0]),
               level="verbose")
        # normalize all paths in output
        for k, v in node[1].items():
            if v is None: node[1][k] = []
        if "output" in node[1]:
            for index, out in enumerate(node[1]['output']):
                node[1]['output'][index] = clean_path(node[1]['output'][index])
        if "dependencies" not in node[1]:
            continue
        sprint("it has dependencies", level="verbose")
        connects = []
        # normalize all paths in dependencies
        for index, dep in enumerate(node[1]['dependencies']):
            dep = os.path.normpath(dep)
            shrt = "dependencies"
            node[1]['dependencies'][index] = clean_path(node[1][shrt][index])
    for node in G.nodes(data=True):
        connects = []
        if "dependencies" not in node[1]:
            continue
        for dep in node[1]['dependencies']:
            matches = check_for_dep_in_outputs(dep, verbose, G)
            if not matches:
                continue
            for match in matches:
                sprint("Appending {} to matches".format(match), level="verbose")
                connects.append(match)
        if connects:
            for connect in connects:
                G.add_edge(connect, node[0])
    return G