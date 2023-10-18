def get_all_dependencies(node_dict):
    """
    ...............................
    """
    deplist = []
    for item in node_dict['dependencies']:
        glist = glob.glob(item)
        if glist:
            for oneglob in glist:
                deplist.append(oneglob)
        else:
            deplist.append(item)
    return deplist