def _set_params(target, param, values, dof):
    '''Set the given param for each of the DOFs for a joint.'''
    if not isinstance(values, (list, tuple, np.ndarray)):
        values = [values] * dof
    assert dof == len(values)
    for s, value in zip(['', '2', '3'][:dof], values):
        target.setParam(getattr(ode, 'Param{}{}'.format(param, s)), value)