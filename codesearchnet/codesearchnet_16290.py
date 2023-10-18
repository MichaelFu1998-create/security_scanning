def get_tied_targets(original_targets, the_ties):
    """
    This function gets called when a target is specified to ensure
    that all 'tied' targets also get included in the subgraph to
    be built
    """
    my_ties = []
    for original_target in original_targets:
        for item in the_ties:
            if original_target in item:
                for thing in item:
                    my_ties.append(thing)
    my_ties = list(set(my_ties))
    if my_ties:
        ties_message = ""
        ties_message += "The following targets share dependencies and must be run together:"
        for item in sorted(my_ties):
            ties_message += "\n  - {}".format(item)
        return list(set(my_ties+original_targets)), ties_message
    return original_targets, ""