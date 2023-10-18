def requirements(debug=True, with_examples=True, with_pgi=None):
    """
    Build requirements based on flags

    :param with_pgi: Use 'pgi' instead of 'gi' - False on CPython, True elsewhere
    :param with_examples:
    :return:
    """
    reqs = list(BASE_REQUIREMENTS)
    if with_pgi is None:
        with_pgi = is_jython

    if debug:
        print("setup options: ")
        print("with_pgi:      ", "yes" if with_pgi else "no")
        print("with_examples: ", "yes" if with_examples else "no")
    if with_pgi:
        reqs.append("pgi")
        if debug:
            print("warning, as of April 2019 typography does not work with pgi")
    else:
        reqs.append(PYGOBJECT)

    if with_examples:
        reqs.extend(EXAMPLE_REQUIREMENTS)

    if debug:
        print("")
        print("")
        for req in reqs:
            print(req)
    return reqs