def check_for_dep_in_outputs(dep, verbose, G):
    """
    Function to help construct_graph() identify dependencies

    Args:
        A dependency
        A flag indication verbosity
        A (populated) NetworkX DiGraph

    Returns:
        A list of targets that build given dependency

    """
    if verbose:
        print("checking dep {}".format(dep))
    ret_list = []
    for node in G.nodes(data=True):
        if "output" not in node[1]:
            continue
        for out in node[1]['output']:
            if fnmatch.fnmatch(out, dep):
                ret_list.append(node[0])
                break
    return ret_list