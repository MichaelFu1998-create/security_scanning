def _get_funky(func):
    """Renvoie une fonction numpy correspondant au nom pass� en param�tre,
    sinon renvoie la fonction elle-m�me"""

    if isinstance(func, str):
        try:
            func = getattr(np, func)
        except:
            raise NameError("Nom de fonction non comprise")
    return func