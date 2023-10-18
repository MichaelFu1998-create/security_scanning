def _get_funky(func):
    """Renvoie une fonction numpy correspondant au nom passé en paramètre,
    sinon renvoie la fonction elle-même"""

    if isinstance(func, str):
        try:
            func = getattr(np, func)
        except:
            raise NameError("Nom de fonction non comprise")
    return func