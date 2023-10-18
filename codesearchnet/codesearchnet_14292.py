def format_pylint_disables(error_names, tag=True):
    """
    Format a list of error_names into a 'pylint: disable=' line.
    """
    tag_str = "lint-amnesty, " if tag else ""
    if error_names:
        return u"  # {tag}pylint: disable={disabled}".format(
            disabled=", ".join(sorted(error_names)),
            tag=tag_str,
        )
    else:
        return ""