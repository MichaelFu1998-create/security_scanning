def MD_restrained(dirname='MD_POSRES', **kwargs):
    """Set up MD with position restraints.

    Additional itp files should be in the same directory as the top file.

    Many of the keyword arguments below already have sensible values. Note that
    setting *mainselection* = ``None`` will disable many of the automated
    choices and is often recommended when using your own mdp file.

    :Keywords:
       *dirname*
          set up under directory dirname [MD_POSRES]
       *struct*
          input structure (gro, pdb, ...) [em/em.pdb]
       *top*
          topology file [top/system.top]
       *mdp*
          mdp file (or use the template) [templates/md.mdp]
       *ndx*
          index file (supply when using a custom mdp)
       *includes*
          additional directories to search for itp files
       *mainselection*
          :program:`make_ndx` selection to select main group ["Protein"]
          (If ``None`` then no canonical index file is generated and
          it is the user's responsibility to set *tc_grps*,
          *tau_t*, and *ref_t* as keyword arguments, or provide the mdp template
          with all parameter pre-set in *mdp* and probably also your own *ndx*
          index file.)
       *deffnm*
          default filename for Gromacs run [md]
       *runtime*
          total length of the simulation in ps [1000]
       *dt*
          integration time step in ps [0.002]
       *qscript*
          script to submit to the queuing system; by default
          uses the template :data:`gromacs.config.qscript_template`, which can
          be manually set to another template from :data:`gromacs.config.templates`;
          can also be a list of template names.
       *qname*
          name to be used for the job in the queuing system [PR_GMX]
       *mdrun_opts*
          option flags for the :program:`mdrun` command in the queuing system
          scripts such as "-stepout 100". [""]
       *kwargs*
          remaining key/value pairs that should be changed in the template mdp
          file, eg ``nstxtcout=250, nstfout=250`` or command line options for
          ``grompp` such as ``maxwarn=1``.

          In particular one can also set **define** and activate
          whichever position restraints have been coded into the itp
          and top file. For instance one could have

             *define* = "-DPOSRES_MainChain -DPOSRES_LIGAND"

          if these preprocessor constructs exist. Note that there
          **must not be any space between "-D" and the value.**

          By default *define* is set to "-DPOSRES".

    :Returns: a dict that can be fed into :func:`gromacs.setup.MD`
              (but check, just in case, especially if you want to
              change the ``define`` parameter in the mdp file)

    .. Note:: The output frequency is drastically reduced for position
              restraint runs by default. Set the corresponding ``nst*``
              variables if you require more output. The `pressure coupling`_
              option *refcoord_scaling* is set to "com" by default (but can
              be changed via *kwargs*) and the pressure coupling
              algorithm itself is set to *Pcoupl* = "Berendsen" to
              run a stable simulation.

    .. _`pressure coupling`: http://manual.gromacs.org/online/mdp_opt.html#pc
    """

    logger.info("[{dirname!s}] Setting up MD with position restraints...".format(**vars()))
    kwargs.setdefault('struct', 'em/em.pdb')
    kwargs.setdefault('qname', 'PR_GMX')
    kwargs.setdefault('define', '-DPOSRES')
    # reduce size of output files
    kwargs.setdefault('nstxout', '50000')   # trr pos
    kwargs.setdefault('nstvout', '50000')   # trr veloc
    kwargs.setdefault('nstfout', '0')       # trr forces
    kwargs.setdefault('nstlog', '500')      # log file
    kwargs.setdefault('nstenergy', '2500')  # edr energy
    kwargs.setdefault('nstxtcout', '5000')  # xtc pos
    # try to get good pressure equilibration
    kwargs.setdefault('refcoord_scaling', 'com')
    kwargs.setdefault('Pcoupl', "Berendsen")

    new_kwargs =  _setup_MD(dirname, **kwargs)

    # clean up output kwargs
    new_kwargs.pop('define', None)          # but make sure that -DPOSRES does not stay...
    new_kwargs.pop('refcoord_scaling', None)
    new_kwargs.pop('Pcoupl', None)
    return new_kwargs