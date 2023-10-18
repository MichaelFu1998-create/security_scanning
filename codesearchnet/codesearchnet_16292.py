def get_all_outputs(node_dict):
    """
    This function takes a node dictionary and returns a list of
    the node's output files. Some of the entries in the 'output'
    attribute may be globs, and without this function, sake won't
    know how to handle that. This will unglob all globs and return
    the true list of *all* outputs.
    """
    outlist = []
    for item in node_dict['output']:
        glist = glob.glob(item)
        if glist:
            for oneglob in glist:
                outlist.append(oneglob)
        else:
            outlist.append(item)
    return outlist