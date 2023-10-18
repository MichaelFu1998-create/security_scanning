def _setup_MD(dirname,
              deffnm='md', mdp=config.templates['md_OPLSAA.mdp'],
              struct=None,
              top='top/system.top', ndx=None,
              mainselection='"Protein"',
              qscript=config.qscript_template, qname=None, startdir=None, mdrun_opts="", budget=None, walltime=1/3.,
              dt=0.002, runtime=1e3, **mdp_kwargs):
    """Generic function to set up a ``mdrun`` MD simulation.

    See the user functions for usage.
    """

    if struct is None:
        raise ValueError('struct must be set to a input structure')
    structure = realpath(struct)
    topology = realpath(top)
    try:
        index = realpath(ndx)
    except AttributeError:  # (that's what realpath(None) throws...)
        index = None        # None is handled fine below

    qname = mdp_kwargs.pop('sgename', qname)    # compatibility for old scripts
    qscript = mdp_kwargs.pop('sge', qscript)    # compatibility for old scripts
    qscript_template = config.get_template(qscript)
    mdp_template = config.get_template(mdp)

    nsteps = int(float(runtime)/float(dt))

    mdp = deffnm + '.mdp'
    tpr = deffnm + '.tpr'
    mainindex = deffnm + '.ndx'
    final_structure = deffnm + '.gro'   # guess... really depends on templates,could also be DEFFNM.pdb

    # write the processed topology to the default output
    mdp_parameters = {'nsteps':nsteps, 'dt':dt, 'pp': 'processed.top'}
    mdp_parameters.update(mdp_kwargs)

    cbook.add_mdp_includes(topology, mdp_parameters)

    logger.info("[%(dirname)s] input mdp  = %(mdp_template)r", vars())
    with in_dir(dirname):
        if not (mdp_parameters.get('Tcoupl','').lower() == 'no' or mainselection is None):
            logger.info("[{dirname!s}] Automatic adjustment of T-coupling groups".format(**vars()))

            # make index file in almost all cases; with mainselection == None the user
            # takes FULL control and also has to provide the template or index
            groups = make_main_index(structure, selection=mainselection,
                                     oldndx=index, ndx=mainindex)
            natoms = {g['name']: float(g['natoms']) for g in groups}
            tc_group_names = ('__main__', '__environment__')   # defined in make_main_index()
            try:
                x = natoms['__main__']/natoms['__environment__']
            except KeyError:
                x = 0   # force using SYSTEM in code below
                wmsg = "Missing __main__ and/or __environment__ index group.\n" \
                       "This probably means that you have an atypical system. You can " \
                       "set mainselection=None and provide your own mdp and index files " \
                       "in order to set up temperature coupling.\n" \
                       "If no T-coupling is required then set Tcoupl='no'.\n" \
                       "For now we will just couple everything to 'System'."
                logger.warn(wmsg)
                warnings.warn(wmsg, category=AutoCorrectionWarning)
            if x < 0.1:
                # couple everything together
                tau_t = firstof(mdp_parameters.pop('tau_t', 0.1))
                ref_t = firstof(mdp_parameters.pop('ref_t', 300))
                # combine all in one T-coupling group
                mdp_parameters['tc-grps'] = 'System'
                mdp_parameters['tau_t'] = tau_t   # this overrides the commandline!
                mdp_parameters['ref_t'] = ref_t   # this overrides the commandline!
                mdp_parameters['gen-temp'] = mdp_parameters.pop('gen_temp', ref_t)
                wmsg = "Size of __main__ is only %.1f%% of __environment__ so " \
                       "we use 'System' for T-coupling and ref_t = %g K and " \
                       "tau_t = %g 1/ps (can be changed in mdp_parameters).\n" \
                       % (x * 100, ref_t, tau_t)
                logger.warn(wmsg)
                warnings.warn(wmsg, category=AutoCorrectionWarning)
            else:
                # couple protein and bath separately
                n_tc_groups = len(tc_group_names)
                tau_t = asiterable(mdp_parameters.pop('tau_t', 0.1))
                ref_t = asiterable(mdp_parameters.pop('ref_t', 300))

                if len(tau_t) != n_tc_groups:
                    tau_t = n_tc_groups * [tau_t[0]]
                    wmsg = "%d coupling constants should have been supplied for tau_t. "\
                        "Using %f 1/ps for all of them." % (n_tc_groups, tau_t[0])
                    logger.warn(wmsg)
                    warnings.warn(wmsg, category=AutoCorrectionWarning)
                if len(ref_t) != n_tc_groups:
                    ref_t = n_tc_groups * [ref_t[0]]
                    wmsg = "%d temperatures should have been supplied for ref_t. "\
                        "Using %g K for all of them." % (n_tc_groups, ref_t[0])
                    logger.warn(wmsg)
                    warnings.warn(wmsg, category=AutoCorrectionWarning)

                mdp_parameters['tc-grps'] = tc_group_names
                mdp_parameters['tau_t'] = tau_t
                mdp_parameters['ref_t'] = ref_t
                mdp_parameters['gen-temp'] = mdp_parameters.pop('gen_temp', ref_t[0])
            index = realpath(mainindex)
        if mdp_parameters.get('Tcoupl','').lower() == 'no':
            logger.info("Tcoupl == no: disabling all temperature coupling mdp options")
            mdp_parameters['tc-grps'] = ""
            mdp_parameters['tau_t'] = ""
            mdp_parameters['ref_t'] = ""
            mdp_parameters['gen-temp'] = ""
        if mdp_parameters.get('Pcoupl','').lower() == 'no':
            logger.info("Pcoupl == no: disabling all pressure coupling mdp options")
            mdp_parameters['tau_p'] = ""
            mdp_parameters['ref_p'] = ""
            mdp_parameters['compressibility'] = ""

        unprocessed = cbook.edit_mdp(mdp_template, new_mdp=mdp, **mdp_parameters)
        check_mdpargs(unprocessed)
        gromacs.grompp(f=mdp, p=topology, c=structure, n=index, o=tpr, **unprocessed)

        runscripts = qsub.generate_submit_scripts(
            qscript_template, deffnm=deffnm, jobname=qname, budget=budget,
            startdir=startdir, mdrun_opts=mdrun_opts, walltime=walltime)

    logger.info("[%(dirname)s] output mdp = %(mdp)r", vars())
    logger.info("[%(dirname)s] output ndx = %(ndx)r", vars())
    logger.info("[%(dirname)s] output tpr = %(tpr)r", vars())
    logger.info("[%(dirname)s] output runscripts = %(runscripts)r", vars())
    logger.info("[%(dirname)s] All files set up for a run time of %(runtime)g ps "
                "(dt=%(dt)g, nsteps=%(nsteps)g)" % vars())

    kwargs = {'struct': realpath(os.path.join(dirname, final_structure)),      # guess
              'top': topology,
              'ndx': index,            # possibly mainindex
              'qscript': runscripts,
              'mainselection': mainselection,
              'deffnm': deffnm,        # return deffnm (tpr = deffnm.tpr!)
              }
    kwargs.update(mdp_kwargs)  # return extra mdp args so that one can use them for prod run
    return kwargs