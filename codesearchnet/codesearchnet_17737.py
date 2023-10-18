def get_command(namespace):
    """
    Get the pylint command for these arguments.

    :param `Namespace` namespace: the namespace
    """
    cmd = ["pylint", namespace.package] + arg_map[namespace.package]
    if namespace.ignore:
        cmd.append("--ignore=%s" % namespace.ignore)
    return cmd