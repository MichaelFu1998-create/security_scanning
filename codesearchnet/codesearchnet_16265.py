def check_integrity(sakefile, settings):
    """
    Checks the format of the sakefile dictionary
    to ensure it conforms to specification

    Args:
        A dictionary that is the parsed Sakefile (from sake.py)
        The setting dictionary (for print functions)
    Returns:
        True if the Sakefile is conformant
        False if not
    """
    sprint = settings["sprint"]
    error = settings["error"]
    sprint("Call to check_integrity issued", level="verbose")
    if not sakefile:
        error("Sakefile is empty")
        return False
    # checking for duplicate targets
    if len(sakefile.keys()) != len(set(sakefile.keys())):
        error("Sakefile contains duplicate targets")
        return False
    for target in sakefile:
        if target == "all":
            if not check_target_integrity(target, sakefile["all"], all=True):
                error("Failed to accept target 'all'")
                return False
            continue
        if "formula" not in sakefile[target]:
            if not check_target_integrity(target, sakefile[target],
                                          meta=True):
                errmes = "Failed to accept meta-target '{}'".format(target)
                error(errmes)
                return False
            for atom_target in sakefile[target]:
                if atom_target == "help":
                    continue
                if not check_target_integrity(atom_target,
                                              sakefile[target][atom_target],
                                              parent=target):
                    errmes = "Failed to accept target '{}'\n".format(
                                                                atom_target)
                    error(errmes)
                    return False
            continue
        if not check_target_integrity(target, sakefile[target]):
            errmes = "Failed to accept target '{}'\n".format(target)
            error(errmes)
            return False
    return True