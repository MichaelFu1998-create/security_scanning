def MD(dirname='MD', **kwargs):
    """Set up equilibrium MD.

    Additional itp files should be in the same directory as the top file.

    Many of the keyword arguments below already have sensible values. Note that
    setting *mainselection* = ``None`` will disable many of the automated
    choices and is often recommended when using your own mdp file.

    :Keywords:
       *dirname*
          set up under directory dirname [MD]
       *struct*
          input structure (gro, pdb, ...) [MD_POSRES/md_posres.pdb]
       *top*
          topology file [top/system.top]
       *mdp*
          mdp file (or use the template) [templates/md.mdp]
       *ndx*
          index file (supply when using a custom mdp)
       *includes*
          additional directories to search for itp files
       *mainselection*
          ``make_ndx`` selection to select main group ["Protein"]
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
          name to be used for the job in the queuing system [MD_GMX]
       *mdrun_opts*
          option flags for the :program:`mdrun` command in the queuing system
          scripts such as "-stepout 100 -dgdl". [""]
       *kwargs*
          remaining key/value pairs that should be changed in the template mdp
          file, e.g. ``nstxtcout=250, nstfout=250`` or command line options for
          :program`grompp` such as ``maxwarn=1``.

    :Returns: a dict that can be fed into :func:`gromacs.setup.MD`
              (but check, just in case, especially if you want to
              change the *define* parameter in the mdp file)
    """

    logger.info("[{dirname!s}] Setting up MD...".format(**vars()))
    kwargs.setdefault('struct', 'MD_POSRES/md.gro')
    kwargs.setdefault('qname', 'MD_GMX')
    return _setup_MD(dirname, **kwargs)