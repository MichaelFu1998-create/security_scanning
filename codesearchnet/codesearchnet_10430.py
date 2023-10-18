def energy_minimize(dirname='em', mdp=config.templates['em.mdp'],
                    struct='solvate/ionized.gro', top='top/system.top',
                    output='em.pdb', deffnm="em",
                    mdrunner=None, mdrun_args=None,
                    **kwargs):
    """Energy minimize the system.

    This sets up the system (creates run input files) and also runs
    ``mdrun_d``. Thus it can take a while.

    Additional itp files should be in the same directory as the top file.

    Many of the keyword arguments below already have sensible values.

    :Keywords:
       *dirname*
          set up under directory dirname [em]
       *struct*
          input structure (gro, pdb, ...) [solvate/ionized.gro]
       *output*
          output structure (will be put under dirname) [em.pdb]
       *deffnm*
          default name for mdrun-related files [em]
       *top*
          topology file [top/system.top]
       *mdp*
          mdp file (or use the template) [templates/em.mdp]
       *includes*
          additional directories to search for itp files
       *mdrunner*
          :class:`gromacs.run.MDrunner` instance; by default we
          just try :func:`gromacs.mdrun_d` and :func:`gromacs.mdrun` but a
          MDrunner instance gives the user the ability to run mpi jobs
          etc. [None]
       *mdrun_args*
          arguments for *mdrunner* (as a dict), e.g. ``{'nt': 2}``;
          empty by default

          .. versionaddedd:: 0.7.0

       *kwargs*
          remaining key/value pairs that should be changed in the
          template mdp file, eg ``nstxtcout=250, nstfout=250``.

    .. note:: If :func:`~gromacs.mdrun_d` is not found, the function
              falls back to :func:`~gromacs.mdrun` instead.
    """

    structure = realpath(struct)
    topology = realpath(top)
    mdp_template = config.get_template(mdp)
    deffnm = deffnm.strip()

    mdrun_args = {} if mdrun_args is None else mdrun_args

    # write the processed topology to the default output
    kwargs.setdefault('pp', 'processed.top')

    # filter some kwargs that might come through when feeding output
    # from previous stages such as solvate(); necessary because *all*
    # **kwargs must be *either* substitutions in the mdp file *or* valid
    # command line parameters for ``grompp``.
    kwargs.pop('ndx', None)
    # mainselection is not used but only passed through; right now we
    # set it to the default that is being used in all argument lists
    # but that is not pretty. TODO.
    mainselection = kwargs.pop('mainselection', '"Protein"')
    # only interesting when passed from solvate()
    qtot = kwargs.pop('qtot', 0)

    # mdp is now the *output* MDP that will be generated from mdp_template
    mdp = deffnm+'.mdp'
    tpr = deffnm+'.tpr'

    logger.info("[{dirname!s}] Energy minimization of struct={struct!r}, top={top!r}, mdp={mdp!r} ...".format(**vars()))

    cbook.add_mdp_includes(topology, kwargs)

    if qtot != 0:
        # At the moment this is purely user-reported and really only here because
        # it might get fed into the function when using the keyword-expansion pipeline
        # usage paradigm.
        wmsg = "Total charge was reported as qtot = {qtot:g} <> 0; probably a problem.".format(**vars())
        logger.warn(wmsg)
        warnings.warn(wmsg, category=BadParameterWarning)

    with in_dir(dirname):
        unprocessed = cbook.edit_mdp(mdp_template, new_mdp=mdp, **kwargs)
        check_mdpargs(unprocessed)
        gromacs.grompp(f=mdp, o=tpr, c=structure, r=structure, p=topology, **unprocessed)
        mdrun_args.update(v=True, stepout=10, deffnm=deffnm, c=output)
        if mdrunner is None:
            mdrun = run.get_double_or_single_prec_mdrun()
            mdrun(**mdrun_args)
        else:
            if type(mdrunner) is type:
                # class
                # user wants full control and provides simulation.MDrunner **class**
                # NO CHECKING --- in principle user can supply any callback they like
                mdrun = mdrunner(**mdrun_args)
                mdrun.run()
            else:
                # anything with a run() method that takes mdrun arguments...
                try:
                    mdrunner.run(mdrunargs=mdrun_args)
                except AttributeError:
                    logger.error("mdrunner: Provide a gromacs.run.MDrunner class or instance or a callback with a run() method")
                    raise TypeError("mdrunner: Provide a gromacs.run.MDrunner class or instance or a callback with a run() method")

        # em.gro --> gives 'Bad box in file em.gro' warning --- why??
        # --> use em.pdb instead.
        if not os.path.exists(output):
            errmsg = "Energy minimized system NOT produced."
            logger.error(errmsg)
            raise GromacsError(errmsg)
        final_struct = realpath(output)

    logger.info("[{dirname!s}] energy minimized structure {final_struct!r}".format(**vars()))
    return {'struct': final_struct,
            'top': topology,
            'mainselection': mainselection,
            }