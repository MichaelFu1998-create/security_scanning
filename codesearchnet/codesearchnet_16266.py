def check_target_integrity(key, values, meta=False, all=False, parent=None):
    """
    Checks the integrity of a specific target. Gets called
    multiple times from check_integrity()

    Args:
        The target name
        The dictionary values of that target
        A boolean representing whether it is a meta-target
        A boolean representing whether it is the "all" target
        A string representing name of parent (default None)

    Returns:
        True is the target is conformant
        False if not
    """

    # logic to audit "all" target
    if all:
        if not values:
            print("Warning: target 'all' is empty")
        # will check if it has unrecognized target later
        return True

    errmes = "target '{}' is not allowed to be missing a help message\n"

    # logic to audit a meta-target
    if meta:
        # check if help is missing
        if "help" not in values:
            sys.stderr.write(errmes.format(key))
            return False
        # checking if empty
        if len(values.keys()) == 1:
            sys.stderr.write("Meta-target '{}' is empty\n".format(key))
            return False
        return True

    # logic to audit any other target
    expected_fields = ["dependencies", "help", "output", "formula"]
    expected_fields = set(expected_fields)
    try:
        our_keys_set = set(values.keys())
    except:
        sys.stderr.write("Error processing target '{}'\n".format(key))
        sys.stderr.write("Are you sure '{}' is a meta-target?\n".format(
                                                                     parent))
        sys.stderr.write("If it's not, it's missing a formula\n")
        return False
    ignored_fields = set([field for field in our_keys_set\
                          if field.strip().startswith("(ignore)")])
    difference = our_keys_set - expected_fields - ignored_fields
    if difference:
        print("The following fields were not recognized and will be ignored")
        for item in difference:
            print("  - " + item)
    if "help" not in values:
        sys.stderr.write(errmes.format(key))
        return False
    # can't be missing formula either
    if "formula" not in values:
        sys.stderr.write("Target '{}' is missing formula\n".format(key))
        return False
    return True