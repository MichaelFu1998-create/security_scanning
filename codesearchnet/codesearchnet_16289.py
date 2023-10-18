def get_ties(G):
    """
    If you specify a target that shares a dependency with another target,
    both targets need to be updated. This is because running one will resolve
    the sha mismatch and sake will think that the other one doesn't have to
    run. This is called a "tie". This function will find such ties.
    """
    # we are going to make a dictionary whose keys are every dependency
    # and whose values are a list of all targets that use that dependency.
    # after making the dictionary, values whose length is above one will
    # be called "ties"
    ties = []
    dep_dict = {}
    for node in G.nodes(data=True):
        if 'dependencies' in node[1]:
            for item in node[1]['dependencies']:
                if item not in dep_dict:
                    dep_dict[item] = []
                dep_dict[item].append(node[0])
    for item in dep_dict:
        if len(list(set(dep_dict[item]))) > 1:
            ties.append(list(set(dep_dict[item])))
    return ties