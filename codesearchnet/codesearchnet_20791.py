def _get_params(target, param, dof):
    '''Get the given param from each of the DOFs for a joint.'''
    return [target.getParam(getattr(ode, 'Param{}{}'.format(param, s)))
            for s in ['', '2', '3'][:dof]]