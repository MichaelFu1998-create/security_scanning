def get_help(sakefile):
    """
    Returns the prettily formatted help strings (for printing)

    Args:
        A dictionary that is the parsed Sakefile (from sake.py)

    NOTE:
        the list sorting in this function is required for this
        function to be deterministic
    """
    full_string = "You can 'sake' one of the following...\n\n"
    errmes = "target '{}' is not allowed to not have help message\n"
    outerlines = []
    for target in sakefile:
        if target == "all":
            # this doesn't have a help message
            continue
        middle_lines = []
        if "formula" not in sakefile[target]:
            # this means it's a meta-target
            innerstr = "{}:\n  - {}\n\n".format(escp(target),
                                                sakefile[target]["help"])
            inner = []
            for atom_target in sakefile[target]:
                if atom_target == "help":
                    continue
                inner.append("    {}:\n      -  {}\n\n".format(escp(atom_target),
                                                               sakefile[target][atom_target]["help"]))
            if inner:
                innerstr += '\n'.join(sorted(inner))
            middle_lines.append(innerstr)
        else:
            middle_lines.append("{}:\n  - {}\n\n".format(escp(target),
                                                         sakefile[target]["help"]))
        if middle_lines:
            outerlines.append('\n'.join(sorted(middle_lines)))

    if outerlines:
        full_string += '\n'.join(sorted(outerlines))
    what_clean_does = "remove all targets' outputs and start from scratch"
    full_string += "\nclean:\n  -  {}\n\n".format(what_clean_does)
    what_visual_does = "output visual representation of project's dependencies"
    full_string += "visual:\n  -  {}\n".format(what_visual_does)
    full_string = re.sub("\n{3,}", "\n\n", full_string)
    return full_string