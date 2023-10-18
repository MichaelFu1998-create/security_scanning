def em_schedule(**kwargs):
    """Run multiple energy minimizations one after each other.

    :Keywords:
      *integrators*
           list of integrators (from 'l-bfgs', 'cg', 'steep')
           [['bfgs', 'steep']]
      *nsteps*
           list of maximum number of steps; one for each integrator in
           in the *integrators* list [[100,1000]]
      *kwargs*
           mostly passed to :func:`gromacs.setup.energy_minimize`

    :Returns: dictionary with paths to final structure ('struct') and
              other files

    :Example:
       Conduct three minimizations:
         1. low memory Broyden-Goldfarb-Fletcher-Shannon (BFGS) for 30 steps
         2. steepest descent for 200 steps
         3. finish with BFGS for another 30 steps
       We also do a multi-processor minimization when possible (i.e. for steep
       (and conjugate gradient) by using a :class:`gromacs.run.MDrunner` class
       for a :program:`mdrun` executable compiled for OpenMP in 64 bit (see
       :mod:`gromacs.run` for details)::

          import gromacs.run
          gromacs.setup.em_schedule(struct='solvate/ionized.gro',
                    mdrunner=gromacs.run.MDrunnerOpenMP64,
                    integrators=['l-bfgs', 'steep', 'l-bfgs'],
                    nsteps=[50,200, 50])

    .. Note:: You might have to prepare the mdp file carefully because at the
              moment one can only modify the *nsteps* parameter on a
              per-minimizer basis.
    """

    mdrunner = kwargs.pop('mdrunner', None)
    integrators = kwargs.pop('integrators', ['l-bfgs', 'steep'])
    kwargs.pop('integrator', None)  # clean input; we set intgerator from integrators
    nsteps = kwargs.pop('nsteps', [100, 1000])

    outputs = ['em{0:03d}_{1!s}.pdb'.format(i, integrator) for i,integrator in enumerate(integrators)]
    outputs[-1] = kwargs.pop('output', 'em.pdb')

    files = {'struct': kwargs.pop('struct', None)}  # fake output from energy_minimize()

    for i, integrator in enumerate(integrators):
        struct = files['struct']
        logger.info("[em %d] energy minimize with %s for maximum %d steps", i, integrator, nsteps[i])
        kwargs.update({'struct':struct, 'output':outputs[i],
                       'integrator':integrator, 'nsteps': nsteps[i]})
        if not integrator == 'l-bfgs':
            kwargs['mdrunner'] = mdrunner
        else:
            kwargs['mdrunner'] = None
            logger.warning("[em %d]  Not using mdrunner for L-BFGS because it cannot "
                           "do parallel runs.", i)

        files = energy_minimize(**kwargs)

    return files