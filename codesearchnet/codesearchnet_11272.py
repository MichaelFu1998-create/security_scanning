def c2u(name):
    """Convert camelCase (used in PHP) to Python-standard snake_case.

    Src:
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    Parameters
    ----------
    name: A function or variable name in camelCase

    Returns
    -------
    str: The name in snake_case

    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return s1