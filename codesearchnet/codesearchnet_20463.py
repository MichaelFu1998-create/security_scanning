def check_pre_requirements(pre_requirements):
    """Check all necessary system requirements to exist.

    :param pre_requirements:
        Sequence of pre-requirements to check by running
        ``where <pre_requirement>`` on Windows and ``which ...`` elsewhere.
    """
    pre_requirements = set(pre_requirements or [])
    pre_requirements.add('virtualenv')

    for requirement in pre_requirements:
        if not which(requirement):
            print_error('Requirement {0!r} is not found in system'.
                        format(requirement))
            return False

    return True