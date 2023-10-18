def pop_param(params):
    """Pops the parameter and the "remainder" (comma, default value).

    Returns a tuple of ('name', default) or (_star, 'name') or (_dstar, 'name').
    """
    default = None

    name = params.pop(0)
    if name in (_star, _dstar):
        default = params.pop(0)
        if default == _comma:
            return name, default

    try:
        remainder = params.pop(0)
        if remainder == _eq:
            default = params.pop(0)
            remainder = params.pop(0)
        if remainder != _comma:
            raise ValueError(f"unexpected token: {remainder}")

    except IndexError:
        pass
    return name, default