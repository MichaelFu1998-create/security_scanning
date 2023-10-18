def needs_to_run(G, target, in_mem_shas, from_store, settings):
    """
    Determines if a target needs to run. This can happen in two ways:
    (a) If a dependency of the target has changed
    (b) If an output of the target is missing

    Args:
        The graph we are going to build
        The name of the target
        The dictionary of the current shas held in memory
        The dictionary of the shas from the shastore
        The settings dictionary

    Returns:
        True if the target needs to be run
        False if not
    """
    force = settings["force"]
    sprint = settings["sprint"]

    if(force):
        sprint("Target rebuild is being forced so {} needs to run".format(target),
               level="verbose")
        return True
    node_dict = get_the_node_dict(G, target)
    if 'output' in node_dict:
        for output in acts.get_all_outputs(node_dict):
            if not os.path.isfile(output):
                outstr = "Output file '{}' is missing so it needs to run"
                sprint(outstr.format(output), level="verbose")
                return True
    if 'dependencies' not in node_dict:
        # if it has no dependencies, it always needs to run
        sprint("Target {} has no dependencies and needs to run".format(target),
               level="verbose")
        return True
    for dep in node_dict['dependencies']:
        # because the shas are updated after all targets build,
        # its possible that the dependency's sha doesn't exist
        # in the current "in_mem" dictionary. If this is the case,
        # then the target needs to run
        if ('files' in in_mem_shas and dep not in in_mem_shas['files'] or
            'files' not in in_mem_shas):
            outstr = "Dep '{}' doesn't exist in memory so it needs to run"
            sprint(outstr.format(dep), level="verbose")
            return True
        now_sha = in_mem_shas['files'][dep]['sha']
        if ('files' in from_store and dep not in from_store['files'] or
            'files' not in from_store):
            outst = "Dep '{}' doesn't exist in shastore so it needs to run"
            sprint(outst.format(dep), level="verbose")
            return True
        old_sha = from_store['files'][dep]['sha']
        if now_sha != old_sha:
            outstr = "There's a mismatch for dep {} so it needs to run"
            sprint(outstr.format(dep), level="verbose")
            return True
    sprint("Target '{}' doesn't need to run".format(target), level="verbose")
    return False