def get_template(t):
    """Find template file *t* and return its real path.

    *t* can be a single string or a list of strings. A string
    should be one of

    1. a relative or absolute path,
    2. a file in one of the directories listed in :data:`gromacs.config.path`,
    3. a filename in the package template directory (defined in the template dictionary
       :data:`gromacs.config.templates`) or
    4. a key into :data:`~gromacs.config.templates`.

    The first match (in this order) is returned. If the argument is a
    single string then a single string is returned, otherwise a list
    of strings.

    :Arguments: *t* : template file or key (string or list of strings)
    :Returns:   os.path.realpath(*t*) (or a list thereof)
    :Raises:    :exc:`ValueError` if no file can be located.

    """
    templates = [_get_template(s) for s in utilities.asiterable(t)]
    if len(templates) == 1:
         return templates[0]
    return templates