def write_tersoff_potential(parameters):
    """Write tersoff potential file from parameters to string

    Parameters
    ----------
    parameters: dict
       keys are tuple of elements with the values being the parameters length 14
    """
    lines = []
    for (e1, e2, e3), params in parameters.items():
        if len(params) != 14:
            raise ValueError('tersoff three body potential expects 14 parameters')
        lines.append(' '.join([e1, e2, e3] + ['{:16.8g}'.format(_) for _ in params]))
    return '\n'.join(lines)